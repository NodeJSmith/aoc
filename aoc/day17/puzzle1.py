from argparse import ArgumentParser
from enum import Enum
from pathlib import Path
from time import sleep

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


CHOICE_MAP = {
    Direction.UP: [Direction.LEFT, Direction.RIGHT, Direction.UP],
    Direction.DOWN: [Direction.LEFT, Direction.RIGHT, Direction.DOWN],
    Direction.LEFT: [Direction.UP, Direction.DOWN, Direction.LEFT],
    Direction.RIGHT: [Direction.UP, Direction.DOWN, Direction.RIGHT],
}


def point_out_of_bounds(point: tuple[int, int], data: np.ndarray):
    return point[0] < 0 or point[1] < 0 or point[0] >= len(data[0]) or point[1] >= len(data)


# switch this to recursion
# track the moves we've made
# detect cycles
# keep grid per recursive call so we can backtrack
# return grid upon succcess or failure so we know how far to backtrack
def move(data: np.ndarray, grid: np.ndarray, start_point: tuple[int, int], start_direction: Direction):
    """
    We start at the top left (0,0) and the goal is to get to the bottom right (len(data[0]), len(data))

    We can only move, at most, three steps in one direction at a time. We can move less than 3 if that is better.
    Each tile has a number, we want to minimize the numbers.

    We cannot move backward. At three consecutive moves in the same direction we must turn left or right.
    """

    stack = [(start_point, start_direction, {d: 0 for d in Direction})]

    while stack:
        curr_point, curr_direction, moves_dict = stack.pop()
        moves_dict = {d: moves_dict[d] + 1 if d == curr_direction else 0 for d in Direction}

        # handle out of bounds
        if point_out_of_bounds(curr_point, data):
            continue

        if args.print:
            sleep(0.1)
            print_colored_array(data, grid, {curr_point: "red"})

        grid[curr_point] = 1
        # find smallest number not backward and not forward, choose that, move again
        # if both are same number, try both
        min_choice = {}
        for choice in CHOICE_MAP[curr_direction]:
            choice_point = tuple(np.array(curr_point) + np.array(choice.value))
            if point_out_of_bounds(choice_point, data) or moves_dict[choice] >= 3:
                continue

            if choice == (len(data[0]), len(data)):
                print("Found the end!")
                return

            val = data[choice_point]
            if not min_choice or val <= min(min_choice.values()):
                min_choice[(choice_point, choice)] = val

        stack.extend((choice_point, choice, moves_dict) for (choice_point, choice) in min_choice)


def main(test: bool = None, print_: bool = None):
    if test is not None:
        args.test = test

    if print_ is not None:
        args.print = print_

    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, args.test).splitlines()
    data = np.array([list(map(int, line)) for line in data])

    grid = np.zeros(shape=(len(data[0]), len(data)), dtype=int)

    if args.print:
        print_colored_array(data, grid, reset_cursor=False)

    move(data, grid, (0, 0), Direction.RIGHT)

    print("\n\n")
    print_colored_array(data, grid, reset_cursor=False)

    sum_grid = np.sum(grid)

    print(f"Sum of illuminated points: {sum_grid}")
    print("\n\n")


if __name__ == "__main__":
    main(test=True, print_=True)
