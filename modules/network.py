import socket
from rich.console import Console
console = Console()

def run():
    host = input("Authorized host: ").strip()
    port = input("TCP port: ").strip()
    try:
        port = int(port)
        with socket.create_connection((host, port), timeout=5):
            console.print("[green]TCP connection successful[/green]")
    except Exception as e:
        console.print(f"[red]Connection failed: {e}[/red]")
