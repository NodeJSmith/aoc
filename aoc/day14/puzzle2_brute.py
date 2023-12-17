from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Literal

from numpy.typing import ArrayLike
from tqdm import tqdm

from aoc_utils import get_data, line_to_list, print_lines

TEST = False
global_idx = 0
SEEN_LINES: dict[tuple[str], list[tuple[str, int]]] = defaultdict(list)


def list_of_lists_to_tuples(lines: list[list[str]]):
    return tuple(map(tuple, lines))


def tuple_of_tuples_to_lists(lines: tuple[tuple[str, ...], ...]):
    return list(map(list, lines))


@lru_cache(maxsize=None)
def transpose_lines(lines: list[list[str]]):
    new_lines = []
    for col in range(len(lines[0])):
        new_line = []
        for row in range(len(lines)):
            new_line.append(lines[row][col])
        new_lines.append(new_line)
    return list_of_lists_to_tuples(new_lines)


@lru_cache(maxsize=None)
def adjust_piece(line: str, direction: Literal["left", "right"]):
    line = line_to_list(line)
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

    piece1 = adjust_piece("".join(part_1), direction)
    piece2 = adjust_piece("".join(part_2), direction)
    return piece1 + piece2


@lru_cache(maxsize=None)
def tilt_lines(lines: ArrayLike, cardinal_direction: str):
    if cardinal_direction.lower() in ["north", "south"]:
        lines = transpose_lines(lines)

    lines = tuple_of_tuples_to_lists(lines)

    offset_direction = "left" if cardinal_direction in ["north", "west"] else "right"

    for i, line in enumerate(lines):
        new_line = adjust_piece("".join(line), offset_direction)
        lines[i] = new_line

    if cardinal_direction.lower() in ["north", "south"]:
        lines = list_of_lists_to_tuples(lines)
        lines = transpose_lines(lines)

    return list_of_lists_to_tuples(lines)


@lru_cache(maxsize=None)
def full_tilt(lines: ArrayLike):
    lines = list_of_lists_to_tuples(lines)
    lines = tilt_lines(lines, "north")
    SEEN_LINES[lines].append(("north", global_idx))
    lines = tilt_lines(lines, "west")
    SEEN_LINES[lines].append(("west", global_idx))
    lines = tilt_lines(lines, "south")
    SEEN_LINES[lines].append(("south", global_idx))

    lines = tilt_lines(lines, "east")
    SEEN_LINES[lines].append(("east", global_idx))
    return list_of_lists_to_tuples(lines)


def main():
    global global_idx
    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, TEST).splitlines()
    lines = list(map(line_to_list, data))
    lines = list_of_lists_to_tuples(lines)

    load_dict = {}
    load_count = defaultdict(int)

    for i in tqdm(range(1_000_000_000)):
        global_idx = i
        lines = full_tilt(lines)
        total_load = get_total_load(lines)
        load_dict[i] = total_load
        load_count[total_load] += 1

    print_lines(lines, wide_mode=False, add_index=False)

    print(get_total_load(lines))


def get_total_load(lines):
    total_load = 0
    for i, line in enumerate(lines):
        load_mult = len(lines) - i
        num_rocks = sum([1 for char in line if char == "O"])
        line_load = num_rocks * load_mult

        total_load += line_load

    return total_load


main()
