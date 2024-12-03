import re
from pathlib import Path

import attrs
from rich.console import Console

from aoc_helper import AocData

CONSOLE = Console()

AOC_DATA = AocData(Path(__file__).resolve().parent)

CONSOLE.print(f"Day {AOC_DATA.day} Part {AOC_DATA.part}")
CONSOLE.print(f"Test Mode: {'Yes' if AOC_DATA.test else 'No'}")
CONSOLE.print(AOC_DATA.data, markup=False)


@attrs.define
class FoundMatch:
    match: str
    a: int
    b: int

    @property
    def result(self):
        return self.a * self.b

    def __str__(self):
        return f"{self.match} = {self.result}"

    def __repr__(self):
        return f"FoundMatch({self.match}, {self.a}, {self.b})"


pattern = re.compile(r"(mul\((\d+),(\d+)\))")

matches = []
for match in pattern.finditer(AOC_DATA.data):
    mul, a, b = match.groups()
    matches.append(FoundMatch(mul, int(a), int(b)))

for m in matches:
    CONSOLE.print(m)

total = sum(match.result for match in matches)
CONSOLE.print(f"Total: {total}")
