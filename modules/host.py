import socket
from rich.console import Console
from modules.validation import normalize_host

console = Console()


def run():
    raw_host = input("Hostname or IP: ").strip()
    try:
        host = normalize_host(raw_host)
        results = sorted({item[4][0] for item in socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)})
        console.print("[green]Resolved addresses:[/green]")
        for address in results:
            console.print(f" • {address}")
    except (ValueError, OSError) as error:
        console.print(f"[red]Resolution failed: {error}[/red]")
