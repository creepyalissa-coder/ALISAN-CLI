import socket
from rich.console import Console
from modules.validation import normalize_host, validate_port

console = Console()


def run():
    raw_host = input("Authorized host: ").strip()
    raw_port = input("TCP port: ").strip()
    try:
        host = normalize_host(raw_host)
        port = validate_port(raw_port)
        with socket.create_connection((host, port), timeout=5):
            console.print("[green]TCP connection successful[/green]")
    except (ValueError, OSError) as error:
        console.print(f"[red]Connection failed: {error}[/red]")
