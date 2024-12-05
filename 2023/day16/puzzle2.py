import sys
from argparse import ArgumentParser
from enum import Enum
from pathlib import Path
from time import sleep

import numpy as np
from aoc_utils import get_data, print_colored_array

parser = ArgumentParser()

parser.add_argument("--test", action="store_true")
parser.add_argument("--print", action="store_true")
parser.add_argument("--print-clean", action="store_true")

args = parser.parse_args()

SAVED_GRIDS = {}


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


def move(data: np.ndarray, grid: np.ndarray, curr_point: tuple[int, int], curr_direction: Direction):
    # handle out of bounds
    if curr_point[0] < 0 or curr_point[1] < 0 or curr_point[0] >= len(data[0]) or curr_point[1] >= len(data):
        return None

    # handle infinite loop
    if (curr_point, curr_direction.value) in TRACKED_POINTS:
        return None

    TRACKED_POINTS.add((curr_point, curr_direction.value))

    if args.print:
        sleep(0.05)
        print_colored_array(data, grid, {curr_point: "red"})
    curr_char = data[curr_point]
    char_type = Char(curr_char)

    # either empty or pointy side of splitter, so continue in same direction
    if char_type == Char.EMPTY or not CHAR_MAP[char_type][curr_direction]:
        # set grid to 1, this element is illuminated
        grid[curr_point] = 1
        return move(data, grid, tuple(np.array(curr_point) + curr_direction.value), curr_direction)

    grid[curr_point] = 1
    for movement in CHAR_MAP[char_type][curr_direction]:
        move(data, grid, tuple(np.array(curr_point) + movement.value), movement)
    return None


def main():
    sys.setrecursionlimit(10000)

    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, args.test).splitlines()
    data = np.array([list(line) for line in data])

    grid = np.zeros(shape=(len(data[0]), len(data)), dtype=int)

    # loop through every edge point and compare all outputs
    starting_points = {
        Direction.LEFT: [(row, data.shape[1] - 1) for row in range(data.shape[0])],
        Direction.DOWN: [(0, col) for col in range(data.shape[1])],
        Direction.UP: [(data.shape[0] - 1, col) for col in range(data.shape[1])],
        Direction.RIGHT: [(row, 0) for row in range(data.shape[0])],
    }

    outputs = {}

    for direction, starting_point in starting_points.items():
        for point in starting_point:
            if args.print:
                print_colored_array(data, grid, reset_cursor=False)
            move(data, grid, point, direction)
            outputs[(point, direction.value)] = curr_score = np.sum(grid)
            print(f"Score for {point} and {direction}: {curr_score}")
            SAVED_GRIDS[(point, direction.value)] = grid.copy()
            grid = np.zeros(shape=(len(data[0]), len(data)), dtype=int)
            TRACKED_POINTS.clear()

    best_score = max(outputs.values())

    best_score_points = [key for key, value in outputs.items() if value == best_score][0]
    best_score_grid = SAVED_GRIDS[best_score_points]

    print("\n\n")

    if args.print_clean:
        for char in Char:
            data[(data == char.value) & (best_score_grid == 1)] = "#"
            data[(data == char.value) & (best_score_grid == 0)] = "."
    print_colored_array(data, best_score_grid, reset_cursor=False)

    print(f"Best score: {best_score}")
    print("\n\n")


if __name__ == "__main__":
    main()
