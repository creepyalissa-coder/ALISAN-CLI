from pathlib import Path
from datetime import datetime

def run():
    Path("reports").mkdir(exist_ok=True)
    files = list(Path("reports").glob("*.txt"))
    output = Path("reports") / "summary.txt"
    output.write_text(
        f"ALISAN CLI REPORT\n{datetime.now()}\n"
        + "\n".join(str(f) for f in files),
        encoding="utf-8"
    )
    print("Report saved:", output)
