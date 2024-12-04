import re
from pathlib import Path

import attrs
from aoc_helper import AocData
from rich.console import Console

CONSOLE = Console()

AOC_DATA = AocData(Path(__file__).resolve().parent)

CONSOLE.print(f"Day {AOC_DATA.day} Part {AOC_DATA.part}")
CONSOLE.print(f"Test Mode: {'Yes' if AOC_DATA.test else 'No'}")
CONSOLE.print(AOC_DATA.data, markup=False)
