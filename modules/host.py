import socket
from rich.console import Console
console = Console()

def run():
    host = input("Hostname or IP: ").strip()
    try:
        print("Resolved:", socket.getaddrinfo(host, None))
    except Exception as e:
        console.print(f"[red]{e}[/red]")
