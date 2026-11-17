import socket
import requests
import dns.resolver
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

def check_domain():
    domain = input("\nEnter domain (example.com): ").strip()

    if not domain or " " in domain:
        console.print("[red]Invalid domain.[/red]")
        return

    results = []
    results.append(f"ALISAN CLI - DOMAIN REPORT")
    results.append(f"Domain: {domain}")
    results.append(f"Date: {datetime.now()}")
    results.append("-" * 40)

    try:
        ip = socket.gethostbyname(domain)
        results.append(f"IPv4: {ip}")
    except Exception:
        results.append("IPv4: Not resolved")

    for record in ["A", "AAAA", "MX", "NS", "TXT"]:
        try:
            answers = dns.resolver.resolve(domain, record)
            results.append(f"\n{record}:")
            for answer in answers:
                results.append(str(answer))
        except Exception:
            results.append(f"\n{record}: No record found")

    try:
        response = requests.get(
            f"https://{domain}",
            timeout=10,
            allow_redirects=True
        )
        results.append(f"\nHTTPS Status: {response.status_code}")
        results.append(f"Final URL: {response.url}")
    except requests.RequestException as error:
        results.append(f"\nHTTPS: Connection failed ({error})")

    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    report_file = report_dir / f"domain_{domain.replace('/', '_')}.txt"
    report_file.write_text("\n".join(results), encoding="utf-8")

    console.print(Panel(
        "\n".join(results),
        title="ALISAN DOMAIN CHECKER",
        border_style="cyan"
    ))
    console.print(f"\n[green]Report saved: {report_file}[/green]")
