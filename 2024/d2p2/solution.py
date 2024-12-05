import argparse
import copy
from itertools import pairwise
from pathlib import Path

from rich.console import Console

parser = argparse.ArgumentParser(description="Day 2 Puzzle 2")
parser.add_argument("--test", "-t", help="Use the test input", action="store_true")

args = parser.parse_args()

CONSOLE = Console()
CURR_DIR = Path(__file__).resolve().parent
INPUT_FILE = CURR_DIR / ("input" if not args.test else "test_input")

DATA = INPUT_FILE.read_text()

REPORTS = [list(map(int, line.split(" "))) for line in DATA.splitlines()]


def subreport_is_safe(report: list[int]):
    all_increasing = all(a < b for a, b in pairwise(report))
    all_decreasing = all(a > b for a, b in pairwise(report))

    if not (all_increasing or all_decreasing):
        return False

    diffs = [abs(b - a) for a, b in pairwise(report)]
    return not max(diffs) > 3


def report_is_safe(report: list[int]):
    orig_report = copy.copy(report)

    orig_report_is_safe = subreport_is_safe(orig_report)
    if orig_report_is_safe:
        CONSOLE.print(f"Safe without removing any levels: {orig_report}")
        return True

    CONSOLE.print("*" * 80)
    for i in range(len(report)):
        report = copy.copy(orig_report)
        report.pop(i)
        pretty_report = copy.copy(orig_report)
        pretty_report = list(map(str, pretty_report))
        pretty_report[i] = f"[red]{pretty_report[i]}[/red]"
        CONSOLE.print(f"Checking level {i} ({pretty_report}): {report}")
        assert report != orig_report
        if subreport_is_safe(report):
            CONSOLE.print(f"Safe after removing level {i} ({orig_report[i]}): {report}")
            CONSOLE.print("*" * 80)
            return True

    CONSOLE.print(f"Unsafe: {orig_report}")
    CONSOLE.print("*" * 80)

    return False


report_statuses = []
for i, report in enumerate(REPORTS):
    status = report_is_safe(report)
    CONSOLE.print(f"{report} -> {status}")
    report_statuses.append((report, status))

total_safe_reports = sum(status for _, status in report_statuses)

CONSOLE.print(f"Total safe reports: {total_safe_reports}")
