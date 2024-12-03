from itertools import pairwise
from pathlib import Path

from rich.console import Console

CONSOLE = Console()
CURR_DIR = Path(__file__).resolve().parent


def report_is_safe(report: list[int]):
    all_increasing = all(a < b for a, b in pairwise(report))
    all_decreasing = all(a > b for a, b in pairwise(report))

    if not (all_increasing or all_decreasing):
        return False

    diffs = [abs(b - a) for a, b in pairwise(report)]
    if max(diffs) > 3:
        return False

    return True


INPUT_FILE = CURR_DIR / "input"

DATA = INPUT_FILE.read_text()

CONSOLE.print(DATA)

REPORTS = [list(map(int, line.split(" "))) for line in DATA.splitlines()]


total_safe_reports = sum(map(report_is_safe, REPORTS))

CONSOLE.print(f"Total safe reports: {total_safe_reports}")
