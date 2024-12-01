import sys
from argparse import ArgumentParser
from enum import Enum
from pathlib import Path

import numpy as np

from aoc_utils import get_data, print_colored_array

parser = ArgumentParser()

parser.add_argument("--test", action="store_true")
parser.add_argument("--print", action="store_true")

args = parser.parse_args()


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Char(Enum):
    VERTICAL = "|"
    HORIZONTAL = "-"
    SLASH = "/"
    BACKSLASH = "\\"
    EMPTY = "."


CHAR_MAP = {
    Char.VERTICAL: {
        Direction.UP: [],
        Direction.DOWN: [],
        Direction.LEFT: [Direction.UP, Direction.DOWN],
        Direction.RIGHT: [Direction.UP, Direction.DOWN],
    },
    Char.HORIZONTAL: {
        Direction.UP: [Direction.LEFT, Direction.RIGHT],
        Direction.DOWN: [Direction.LEFT, Direction.RIGHT],
        Direction.LEFT: [],
        Direction.RIGHT: [],
    },
    Char.SLASH: {
        Direction.UP: [Direction.RIGHT],
        Direction.DOWN: [Direction.LEFT],
        Direction.LEFT: [Direction.DOWN],
        Direction.RIGHT: [Direction.UP],
    },
    Char.BACKSLASH: {
        Direction.UP: [Direction.LEFT],
        Direction.DOWN: [Direction.RIGHT],
        Direction.LEFT: [Direction.UP],
        Direction.RIGHT: [Direction.DOWN],
    },
}

TRACKED_POINTS = set()


def move_iteratively(data: np.ndarray, grid: np.ndarray, start_point: tuple[int, int], start_direction: Direction):
    stack = [(start_point, start_direction)]

    while stack:
        curr_point, curr_direction = stack.pop()

        # handle out of bounds
        if curr_point[0] < 0 or curr_point[1] < 0 or curr_point[0] >= len(data[0]) or curr_point[1] >= len(data):
            continue

        # handle infinite loop
        if (curr_point, curr_direction.value) in TRACKED_POINTS:
            continue

        TRACKED_POINTS.add((curr_point, curr_direction.value))

        if args.print:
            print_colored_array(data, grid, {curr_point: "red"})
        curr_char = data[curr_point]
        char_type = Char(curr_char)

        grid[curr_point] = 1

        # either empty or pointy side of splitter, so continue in same direction
        if char_type == Char.EMPTY or not CHAR_MAP[char_type][curr_direction]:
            next_point = tuple(np.array(curr_point) + curr_direction.value)
            stack.append((next_point, curr_direction))
        else:
            for movement in CHAR_MAP[char_type][curr_direction]:
                next_point = tuple(np.array(curr_point) + movement.value)
                stack.append((next_point, movement))


def main():
    sys.setrecursionlimit(10000)

    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, args.test).splitlines()
    data = np.array([list(line) for line in data])

    grid = np.zeros(shape=(len(data[0]), len(data)), dtype=int)

    if args.print:
        print_colored_array(data, grid, reset_cursor=False)

    move_iteratively(data, grid, (0, 0), Direction.RIGHT)

    for char in Char:
        data[(data == char.value) & (grid == 1)] = "#"
        data[(data == char.value) & (grid == 0)] = "."

    print("\n\n")
    print_colored_array(data, grid, reset_cursor=False)

    sum_grid = np.sum(grid)

    print(f"Sum of illuminated points: {sum_grid}")
    print("\n\n")


if __name__ == "__main__":
    main()
