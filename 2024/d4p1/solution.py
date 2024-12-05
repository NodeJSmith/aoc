from copy import deepcopy
from pathlib import Path

from rich.console import Console

from aoc_helper import AocData

CONSOLE = Console()

AOC_DATA = AocData(Path(__file__).resolve().parent)

AOC_DATA.print(f"Day {AOC_DATA.day} Part {AOC_DATA.part}")
AOC_DATA.print(f"Test Mode: {'Yes' if AOC_DATA.args.test else 'No'}")
AOC_DATA.print(AOC_DATA.data, markup=False)

pos_x: set[tuple[int, int]] = set()

for i, line in enumerate(AOC_DATA.data.splitlines()):
    for j, char in enumerate(line):
        if char == "X":
            pos_x.add((i, j))


AOC_DATA.print(pos_x)

raw_data = [list(x) for x in AOC_DATA.data.splitlines()]
all_coords = set((i, j) for i in range(len(raw_data)) for j in range(len(raw_data[0])))

start = (0, 0)  # Starting coordinate
steps = {}

steps["moving_up"] = [(start[0] + i, start[1]) for i in range(0, 4)]
steps["moving_right"] = [(start[0], start[1] - i) for i in range(0, 4)]
steps["moving_left"] = [(start[0], start[1] + i) for i in range(0, 4)]
steps["moving_down"] = [(start[0] - i, start[1]) for i in range(0, 4)]
steps["moving_up_left"] = [(start[0] + i, start[1] + i) for i in range(0, 4)]
steps["moving_up_right"] = [(start[0] + i, start[1] - i) for i in range(0, 4)]
steps["moving_down_left"] = [(start[0] - i, start[1] + i) for i in range(0, 4)]
steps["moving_down_right"] = [(start[0] - i, start[1] - i) for i in range(0, 4)]

desired_char_map = {0: "X", 1: "M", 2: "A", 3: "S"}
all_found_coords = set()

num_found = 0
for coord in pos_x:
    if AOC_DATA.args.test or AOC_DATA.args.force_print:
        pretty_data = deepcopy(raw_data)
        char = raw_data[coord[0]][coord[1]]
        pretty_data[coord[0]][coord[1]] = f"[green]{char}[/green]"
        AOC_DATA.print()
        AOC_DATA.print(f"Checking {coord}")
        AOC_DATA.print("\n".join([" ".join(x) for x in pretty_data]))
        AOC_DATA.print()

    for step_name, step_list in steps.items():
        if AOC_DATA.args.test or AOC_DATA.args.force_print:
            AOC_DATA.print(f"Checking {step_name}")
            pretty_data = deepcopy(raw_data)
        found_coords = set()
        for i, step in enumerate(step_list):
            offset_coord = (coord[0] - step[0], coord[1] - step[1])
            if offset_coord[0] < 0 or offset_coord[1] < 0:
                break
            if offset_coord[0] >= len(raw_data) or offset_coord[1] >= len(raw_data[0]):
                break

            char = raw_data[offset_coord[0]][offset_coord[1]]
            desired_char = desired_char_map[i]

            if char != desired_char:
                break

            if AOC_DATA.args.test or AOC_DATA.args.force_print:
                pretty_data[offset_coord[0]][offset_coord[1]] = f"[green]{char}[/green]"
            found_coords.add(offset_coord)

            if desired_char == "S":
                num_found += 1
                # AOC_DATA.print(f"Found at {offset_coord}")
                # break
                AOC_DATA.print()
                AOC_DATA.print(f"Found by {step_name}")
                if AOC_DATA.args.test or AOC_DATA.args.force_print:
                    AOC_DATA.print("\n".join([" ".join(x) for x in pretty_data]))
                AOC_DATA.print()

                all_found_coords.update(found_coords)


AOC_DATA.force_print(f"Found {num_found} matches")

pretty_data = deepcopy(raw_data)
for coord in all_coords:
    if coord not in all_found_coords:
        pretty_data[coord[0]][coord[1]] = "."


AOC_DATA.print("\n".join([" ".join(x) for x in pretty_data]))
