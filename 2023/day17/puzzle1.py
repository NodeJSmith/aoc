from argparse import ArgumentParser
from collections import defaultdict
from enum import Enum
from heapq import heappop, heappush
from pathlib import Path

import numpy as np
from aoc_utils import get_data, point_out_of_bounds, print_colored_array

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


def get_path(curr_node, tracked):
    path = [curr_node]
    node = tracked[curr_node]
    while node is not None:
        path.append(node)
        node = tracked.get(node)
    return path


def get_min_heat_loss(data: np.ndarray, source: tuple[int, int], target: tuple[int, int]):
    push = heappush
    pop = heappop

    start_item = (source, Direction.RIGHT.value, 0)

    queue = [(0, *start_item)]
    tracked: dict[tuple[int, tuple[int, int], Direction, int], int] = defaultdict(lambda: 10_000)

    path = {start_item: None}
    tracked[start_item] = 0

    reset_cursor = False
    while queue:
        # Pop the smallest item from queue.
        heat_loss, curr_node, direction, consecutive = pop(queue)

        if curr_node == target:
            print_path(data, path, reset_cursor, curr_node, direction, consecutive)
            return heat_loss

        if args.print:
            # time.sleep(0.1)
            print_path(data, path, reset_cursor, curr_node, direction, consecutive)
            reset_cursor = True

        for new_direction in CHOICE_MAP[Direction(direction)]:
            if direction == new_direction.value:
                if consecutive == 3:
                    continue
                new_consecutive = consecutive + 1
            else:
                new_consecutive = 1

            neighbor = tuple(np.add(curr_node, new_direction.value))
            if point_out_of_bounds(neighbor, data):
                continue

            new_heat_loss = heat_loss + int(data[neighbor])

            new_item = (neighbor, new_direction.value, new_consecutive)
            if new_heat_loss < tracked[new_item]:
                tracked[new_item] = new_heat_loss
                path[new_item] = (curr_node, direction, consecutive)
                push(queue, (new_heat_loss, *new_item))
    return None


def print_path(data, path, reset_cursor, curr_node, direction, consecutive):
    curr_path = get_path((curr_node, direction, consecutive), path)

    # colored_points = {k: "blue" for k in explored}
    colored_points = {k[0]: "red" for k in curr_path}
    colored_points.update({curr_node: "green"})

    print_colored_array(data, None, colored_points, reset_cursor=reset_cursor)
    reset_cursor = True


def find_shortest_path(data: np.ndarray):
    start_point = (0, 0)
    end_point = (len(data[0]) - 1, len(data) - 1)

    min_val = get_min_heat_loss(data, start_point, end_point)

    return min_val


def main(test: bool | None = None, print_: bool | None = None):
    if test is not None:
        args.test = test

    if print_ is not None:
        args.print = print_

    print(args)

    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, args.test).splitlines()
    data = np.array([list(map(int, line)) for line in data])

    shortest_path = find_shortest_path(data)

    print(f"Shortest path: {shortest_path}")


if __name__ == "__main__":
    main()
