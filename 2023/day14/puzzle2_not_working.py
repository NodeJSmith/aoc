from functools import lru_cache
from pathlib import Path
from typing import Literal

from numpy.typing import ArrayLike

from aoc_utils import get_data, line_to_list

TEST = False

SEEN_LINES: set[tuple[str, ...]] = set()


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
    lines = tilt_lines(lines, "west")
    lines = tilt_lines(lines, "south")
    lines = tilt_lines(lines, "east")
    return list_of_lists_to_tuples(lines)


def get_total_load(lines):
    total_load = 0
    for i, line in enumerate(lines):
        load_mult = len(lines) - i
        num_rocks = sum([1 for char in line if char == "O"])
        line_load = num_rocks * load_mult

        total_load += line_load

    return total_load


def find_pattern(result_list):
    potential_patterns = []
    for i, result in enumerate(result_list):
        if result_list.count(result) > 1:
            total_load = get_total_load(result)
            potential_patterns.append((result, i, result_list.count(result), total_load))

    return potential_patterns


potential_finals = []

all_results = []

ANSWER = 102943


def main():
    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, TEST).splitlines()
    lines = list(map(line_to_list, data))
    lines = list_of_lists_to_tuples(lines)

    for i in range(1_000_000_000):
        lines = full_tilt(lines)

        if (1_000_000_000 - i) % (all_results.index(lines) - i) == 0:
            break

        total_load = get_total_load(lines)

    print(total_load)


main()

# this broke somewhere along the way, not sure where
