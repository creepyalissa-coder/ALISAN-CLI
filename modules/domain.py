import socket
from datetime import datetime
from pathlib import Path

import dns.resolver
import requests
from rich.console import Console
from rich.panel import Panel

from modules.validation import normalize_host, resolve_public_addresses, validate_https_url

console = Console()


def check_domain():
    raw_domain = input("\nEnter domain (example.com): ").strip()
    try:
        domain = normalize_host(raw_domain)
    except ValueError as error:
        console.print(f"[red]{error}[/red]")
        return

    results = ["ALISAN CLI - DOMAIN REPORT", f"Domain: {domain}", f"Date: {datetime.now().astimezone().isoformat()}", "-" * 40]
    try:
        results.append("Resolved IPs: " + ", ".join(resolve_public_addresses(domain)))
    except ValueError as error:
        results.append(f"Address validation: {error}")

    for record in ("A", "AAAA", "MX", "NS", "TXT"):
        try:
            answers = dns.resolver.resolve(domain, record, lifetime=4)
            results.append(f"\n{record}:")
            results.extend(str(answer) for answer in answers)
        except Exception:
            results.append(f"\n{record}: No record found or DNS query failed")

    # Do not follow redirects: a redirect could point to an internal service.
    try:
        safe_url = validate_https_url(f"https://{domain}")
        response = requests.get(safe_url, timeout=(4, 8), allow_redirects=False, stream=True)
        results.append(f"\nHTTPS Status: {response.status_code}")
        if 300 <= response.status_code < 400:
            results.append("Redirect: not followed (manual review required)")
        response.close()
    except (ValueError, requests.RequestException) as error:
        results.append(f"\nHTTPS: Not checked ({error})")

    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    report_file = report_dir / f"domain_{domain.replace(':', '_')}.txt"
    report_file.write_text("\n".join(results), encoding="utf-8")
    console.print(Panel("\n".join(results), title="ALISAN DOMAIN CHECKER", border_style="cyan"))
    console.print(f"\n[green]Report saved: {report_file}[/green]")
