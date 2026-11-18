from rich.console import Console
from rich.panel import Panel

from modules.host import run as host_run
from modules.domain import check_domain
from modules.network import run as network_run
from modules.security import run as security_run
from modules.reports import run as reports_run

console = Console()

def main():
    while True:
        console.print(Panel.fit(
            "[bold cyan]ALISAN CLI[/bold cyan]\n"
            "[green]Cyber Infrastructure & Intelligence Toolkit[/green]\n"
            "[dim]Version 1.2.0 | Alisan Tech[/dim]",
            border_style="cyan"
        ))

        console.print("""
[cyan]1[/cyan] Host Manager
[cyan]2[/cyan] Domain Checker
[cyan]3[/cyan] Network Tools
[cyan]4[/cyan] Security Scanner
[cyan]5[/cyan] Report Engine
[cyan]0[/cyan] Exit
""")

        choice = input("ALISAN > ").strip()

        if choice == "0":
            break
        elif choice == "1":
            host_run()
        elif choice == "2":
            check_domain()
        elif choice == "3":
            network_run()
        elif choice == "4":
            security_run()
        elif choice == "5":
            reports_run()
        else:
            console.print("[red]Invalid selection[/red]")

if __name__ == "__main__":
    main()
