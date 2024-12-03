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
ENABLE_STR_PATTERN = re.compile(r"(don't|do)")
MUL_PATTERN = re.compile(r"(mul\((\d+),(\d+)\))")


@attrs.define
class FoundMatch:
    is_enabled: bool
    match: str
    a: int
    b: int

    @property
    def result(self):
        return self.a * self.b if self.is_enabled else 0

    def __str__(self):
        return f"{self.match} = {self.result}"

    def __repr__(self):
        return f"FoundMatch({self.match}, {self.a}, {self.b})"


def get_enabled_dict():
    enable_matches = {0: True}
    for match in ENABLE_STR_PATTERN.finditer(AOC_DATA.data):
        enable_str = match.group(1)
        pos = match.end()
        # enable_matches.append(enable_str)
        is_enabled = enable_str == "do"
        enable_matches[pos] = is_enabled

    CONSOLE.print(enable_matches)

    return enable_matches


enable_matches = get_enabled_dict()


def get_matches():
    matches: list[FoundMatch] = []
    is_enabled = True
    for match in MUL_PATTERN.finditer(AOC_DATA.data):
        curr_pos = match.start()
        if len(enable_matches):
            min_enable_pos = min(enable_matches.keys())
            if curr_pos > min_enable_pos:
                prev_is_enabled = is_enabled
                is_enabled = enable_matches[min_enable_pos]
                enable_matches.pop(min_enable_pos)
                if prev_is_enabled != is_enabled:
                    CONSOLE.print(f"Switching to: {is_enabled}")
                else:
                    CONSOLE.print(f"Keeping: {is_enabled}")
                CONSOLE.print(f"Popping: {min_enable_pos}")

        mul, a, b = match.groups()
        fm = FoundMatch(is_enabled, mul, int(a), int(b))
        matches.append(fm)
        CONSOLE.print(fm)

    return matches


matches = get_matches()
total = sum(match.result for match in matches)
CONSOLE.print(f"Total: {total}")
