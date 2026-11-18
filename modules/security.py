import requests
from rich.console import Console
from modules.validation import validate_https_url

console = Console()
HEADERS = (
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
)


def run():
    raw_url = input("Authorized HTTPS URL: ").strip()
    try:
        url = validate_https_url(raw_url)
        response = requests.get(url, timeout=(4, 8), allow_redirects=False, stream=True)
        console.print(f"HTTP status: {response.status_code}")
        if 300 <= response.status_code < 400:
            console.print("[yellow]Redirect not followed; inspect Location manually.[/yellow]")
        for header in HEADERS:
            value = response.headers.get(header)
            console.print(f"{header}: {value if value else '[MISSING]'}")
        response.close()
        console.print("[dim]This is a security-header presence check, not a vulnerability scan.[/dim]")
    except (ValueError, requests.RequestException) as error:
        console.print(f"[red]Request not completed: {error}[/red]")
