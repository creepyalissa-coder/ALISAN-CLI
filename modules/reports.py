from datetime import datetime
from pathlib import Path


def run():
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    files = sorted(path for path in report_dir.glob("*.txt") if path.name != "summary.txt")
    output = report_dir / "summary.txt"
    lines = ["ALISAN CLI REPORT INDEX", datetime.now().astimezone().isoformat(), f"Reports found: {len(files)}", ""]
    lines.extend(f"- {path.name} ({path.stat().st_size} bytes)" for path in files)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Report saved:", output)
