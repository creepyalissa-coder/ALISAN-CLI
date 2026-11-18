"""Input validation helpers for ALISAN-CLI."""
import ipaddress
import re
import socket
from urllib.parse import urlsplit

_DOMAIN_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$", re.I)


def normalize_host(value: str) -> str:
    value = (value or "").strip().rstrip(".")
    if not value or any(ch.isspace() for ch in value) or len(value) > 253:
        raise ValueError("Invalid hostname or IP address")
    try:
        return str(ipaddress.ip_address(value))
    except ValueError:
        pass
    try:
        ascii_host = value.encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise ValueError("Invalid internationalized domain name") from exc
    if not ascii_host or any(not _DOMAIN_LABEL.fullmatch(label) for label in ascii_host.split(".")):
        raise ValueError("Invalid hostname")
    if "." not in ascii_host and ascii_host != "localhost":
        raise ValueError("A fully qualified hostname is required")
    if ascii_host == "localhost" or ascii_host.endswith(".localhost") or ascii_host.endswith(".local"):
        raise ValueError("Local hostnames are not accepted here")
    return ascii_host


def validate_port(value) -> int:
    try:
        port = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Port must be an integer") from exc
    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535")
    return port


def resolve_public_addresses(host: str):
    """Resolve host and reject the whole result if any address is non-global."""
    normalized = normalize_host(host)
    try:
        literal = ipaddress.ip_address(normalized)
        addresses = [literal]
    except ValueError:
        try:
            records = socket.getaddrinfo(normalized, None, type=socket.SOCK_STREAM)
            addresses = list({ipaddress.ip_address(item[4][0]) for item in records})
        except (OSError, ValueError) as exc:
            raise ValueError("Hostname could not be resolved") from exc
    if not addresses:
        raise ValueError("Hostname returned no IP addresses")
    if any(not address.is_global for address in addresses):
        raise ValueError("Target resolves to a private, local, reserved, or non-global IP address")
    return sorted({str(address) for address in addresses})


def validate_https_url(value: str) -> str:
    value = (value or "").strip()
    try:
        parsed = urlsplit(value)
        if parsed.scheme.lower() != "https" or not parsed.hostname:
            raise ValueError
        if parsed.username is not None or parsed.password is not None:
            raise ValueError
        if parsed.port not in (None, 443):
            raise ValueError
        if parsed.query and len(parsed.query) > 2048:
            raise ValueError
        host = normalize_host(parsed.hostname)
        resolve_public_addresses(host)
    except (ValueError, UnicodeError) as exc:
        raise ValueError("Enter a valid HTTPS URL on a public host (port 443 only)") from exc
    path = parsed.path or "/"
    return f"https://{host}{path}" + (f"?{parsed.query}" if parsed.query else "")
