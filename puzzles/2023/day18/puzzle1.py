from pathlib import Path

import numpy as np

from aoc_utils import (
    Direction,
    first_nonzero_col,
    first_nonzero_row,
    get_data,
    last_nonzero_col,
    last_nonzero_row,
    point_out_of_bounds,
    print_colored_array,
)

colored_points = {}
FILL_CHAR = " "
MOVE_MAP = {"D": Direction.DOWN, "U": Direction.UP, "L": Direction.LEFT, "R": Direction.RIGHT}


def flood_fill(grid, point: tuple[int, int], fill_char=FILL_CHAR):
    fill_queue = [point]

    while len(fill_queue) > 0:
        point = fill_queue.pop(0)
        if point_out_of_bounds(point, grid):
            continue
        if grid[point] == "#" or grid[point] == fill_char:
            continue

        grid[point] = fill_char

        for d in Direction:
            fill_queue.append(tuple(np.add(point, d.value)))


def perform_flood_fill_from_edges(grid: np.ndarray):
    for column in range(grid.shape[0]):
        flood_fill(grid, (column, 0))
        flood_fill(grid, (column, grid.shape[1] - 1))

    for row in range(grid.shape[1]):
        flood_fill(grid, (0, row))
        flood_fill(grid, (grid.shape[0] - 1, row))


def convert_and_print_grid(grid: np.ndarray, colored_points: dict[tuple[int, int], str]):
    new_grid = convert_grid(grid)

    print_colored_array(new_grid, colored_points=colored_points, reset_cursor=False)


def convert_grid(grid: np.ndarray):
    new_grid = np.zeros(grid.shape, dtype=str)
    new_grid[grid == 0] = "."
    new_grid[grid == 1] = "#"
    return new_grid


def move_direction(curr_loc: tuple[int, int], direction: Direction):
    return (curr_loc[0] + direction.value[0], curr_loc[1] + direction.value[1])


def move_direction_n_times(data: np.ndarray, curr_loc: tuple[int, int], direction: Direction, n: int, hex_color: str):
    for _ in range(n):
        data[curr_loc] = 1
        curr_loc = move_direction(curr_loc, direction)
        colored_points[curr_loc] = hex_color
    return curr_loc


too_low_answers = [45_945]

curr_dir = Path(__file__).parent.absolute()

data = get_data(curr_dir, False).splitlines()

max_val = 0
for line in data:
    direction, value, *rest = line.split()
    max_val += int(value)


zeroes = np.zeros((max_val * 2, max_val * 2), dtype=int)


curr_loc = (zeroes.shape[0] // 2, zeroes.shape[1] // 2)
for line in data:
    direction, value, rest = line.split()
    hex_color = rest.replace("(", "").replace(")", "")

    curr_loc = move_direction_n_times(zeroes, curr_loc, MOVE_MAP[direction], int(value), hex_color)


offset = (first_nonzero_row(zeroes), first_nonzero_col(zeroes))
zeroes = zeroes[offset[0] : last_nonzero_row(zeroes) + 1, offset[1] : last_nonzero_col(zeroes) + 1]
colored_points = {tuple(np.subtract(k, offset)): v for k, v in colored_points.items()}

grid = convert_grid(zeroes)
print_colored_array(grid, colored_points=colored_points, reset_cursor=False)
perform_flood_fill_from_edges(grid)

print_colored_array(grid, colored_points=colored_points, reset_cursor=False)

ones_grid = np.zeros(grid.shape, dtype=int)
ones_grid[grid == "#"] = 1
ones_grid[grid == "."] = 1

answer = np.sum(ones_grid)
print(f"Answer: {answer}")

if answer <= min(too_low_answers):
    print("Too low!")
