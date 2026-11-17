import requests
from rich.console import Console
console = Console()

def run():
    url = input("Authorized HTTPS URL: ").strip()
    if not url.startswith("https://"):
        console.print("[red]HTTPS URL required[/red]")
        return
    try:
        r = requests.get(url, timeout=10)
        for h in ["Strict-Transport-Security", "Content-Security-Policy",
                  "X-Content-Type-Options", "X-Frame-Options"]:
            console.print(f"{h}: {r.headers.get(h, 'MISSING')}")
    except requests.RequestException as e:
        console.print(f"[red]{e}[/red]")
