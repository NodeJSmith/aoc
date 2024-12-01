from collections import Counter
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


list_one_counter, list_two_counter = Counter(list_one), Counter(list_two)

sim_scores = []
for item in list_one:
    # list_one_value = list_one_counter.get(item, 0)
    list_two_value = list_two_counter.get(item, 0)

    sim_score = item * list_two_value

    CONSOLE.print(f"{item} * {list_two_value} = {sim_score}")

    sim_scores.append(sim_score)


total = sum(sim_scores)
CONSOLE.print(total)
