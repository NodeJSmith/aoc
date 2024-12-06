from pathlib import Path

from ordered_set import OrderedSet
from rich.console import Console

from aoc_helper import AocData

CONSOLE = Console()

AOC_DATA = AocData(Path(__file__).resolve().parent)

AOC_DATA.print(f"Day {AOC_DATA.day} Part {AOC_DATA.part}")
AOC_DATA.print(f"Test Mode: {'Yes' if AOC_DATA.args.test else 'No'}")
AOC_DATA.print(AOC_DATA.data)

rules: list[OrderedSet[int]] = []
for line in AOC_DATA.data.splitlines():
    if not line:
        break
    rules.append(OrderedSet(map(int, line.split("|"))))

AOC_DATA.print(rules)
