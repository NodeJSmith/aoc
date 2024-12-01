from pathlib import Path
from typing import Literal

from aoc_utils import get_data, line_to_list, print_lines

TEST = False


def get_line_dict():
    line_dict: dict[str, list[int]] = {}

    for line in data:
        pattern, hint = line.split(" ")
        line_dict[pattern] = list(map(int, hint.split(",")))

    return line_dict


def flip_rows_to_cols(lines: list[list[str]]):
    new_lines = []
    for col in range(len(lines[0])):
        new_line = []
        for row in range(len(lines)):
            new_line.append(lines[row][col])
        new_lines.append(new_line)
    return new_lines


curr_dir = Path(__file__).parent.absolute()

data = get_data(curr_dir, TEST).splitlines()
lines = list(map(line_to_list, data))
print_lines(lines, wide_mode=False, add_index=False)

flipped_lines = flip_rows_to_cols(lines)


def adjust_piece(line, direction: Literal["left", "right"]):
    if "O" not in line:
        return line

    if "#" not in line:
        period_count = len([char for char in line if char == "."])
        o_count = len([char for char in line if char == "O"])
        if direction == "left":
            new_line = ["O"] * o_count + ["."] * period_count
        else:
            new_line = ["."] * period_count + ["O"] * o_count

        return new_line

    hash_index = "".join(line).find("#")
    hash_index = hash_index + 1 if hash_index == 0 else hash_index
    part_1 = line[:hash_index]
    part_2 = line[hash_index:]

    piece1 = adjust_piece(part_1, direction)
    piece2 = adjust_piece(part_2, direction)
    return piece1 + piece2


for i, line in enumerate(flipped_lines):
    print("before:", line)
    new_line = adjust_piece(line, "left")
    flipped_lines[i] = new_line
    print("after: ", new_line)
    print()


flipped_lines = flip_rows_to_cols(flipped_lines)

print_lines(flipped_lines, wide_mode=False, add_index=False)
total_load = 0
for i, line in enumerate(flipped_lines):
    load_mult = len(flipped_lines) - i
    num_rocks = sum([1 for char in line if char == "O"])
    line_load = num_rocks * load_mult

    total_load += line_load

print(total_load)
