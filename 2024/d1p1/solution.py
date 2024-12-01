from pathlib import Path

from rich.console import Console

CONSOLE = Console()
CURR_DIR = Path(__file__).resolve().parent

input_file = CURR_DIR / "input"

data = input_file.read_text()

CONSOLE.print(data)

# split each line on '  ', append first portion to one list, second portion to another list
# zip the two lists together and iterate over them

list_one, list_two = [], []

for line in data.splitlines():
    one, two = map(int, line.split("  "))
    list_one.append(one)
    list_two.append(two)


list_one, list_two = sorted(list_one), sorted(list_two)

diffs = [abs(one - two) for one, two in zip(list_one, list_two)]

total = sum(diffs)

CONSOLE.print(total)
