import math
from collections import deque
from enum import Enum
from pathlib import Path
from typing import Optional, Union

from rich.console import Console

console = Console(highlight=False)
TEST = False
TEST_INPUT_FILE = "test_input2"
S = "|" if not TEST else "F"
curr_dir = Path(__file__).parent
COLORS = range(125, 160)

PATH_DEQUE = deque(maxlen=4)

"""

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile,
but your sketch doesn't show what shape the pipe has.

"""


class Grid:
    def __init__(self, lines: list[list[str]]):
        self.lines = lines


class Point:
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __init__(self, x: int, y: int, lines: Optional[list[str]] = None):
        self.x = x
        self.y = y
        self.lines = lines

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Point):
            return self.x == o.x and self.y == o.y
        elif isinstance(o, tuple):
            return self.x == o[0] and self.y == o[1]

    def __repr__(self) -> str:
        return tuple((self.x, self.y)).__repr__()

    def __sub__(self, o: object) -> "Point":
        if not isinstance(o, Point):
            raise TypeError(f"Cannot subtract {type(o)} from Point")
        return Point(self.x - o.x, self.y - o.y, self.lines or o.lines)

    def __add__(self, o: object) -> "Point":
        if not isinstance(o, Point):
            raise TypeError(f"Cannot add {type(o)} to Point")
        if self.lines is None:
            lines = o.lines
        else:
            lines = self.lines
        return Point(self.x + o.x, self.y + o.y, lines)

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def get_offset_point(self, direction: Union["Direction", "Point"]):
        if isinstance(direction, Direction):
            return self + direction.value
        elif isinstance(direction, Point):
            return self + direction
        else:
            raise TypeError(f"Cannot add {type(direction)} to Point")

    @property
    def char(self):
        return self.lines[self.y][self.x]

    def print_point_and_next_point_on_grid(self, next_point: "Point"):
        print()
        if PATH_DEQUE and PATH_DEQUE[-1] != self:
            PATH_DEQUE.append(self)
        PATH_DEQUE.append(self + next_point)
        print_centered_subgrid(self.lines, self.x, self.y, 6)
        print()


def print_centered_subgrid(grid: list[list[str]], center_x: int, center_y: int, subgrid_size: int):
    grid_height = len(grid)
    grid_width = len(grid[0]) if grid_height > 0 else 0

    half_subgrid_size = subgrid_size // 2

    # Calculate start and end indices for rows and columns
    start_row = max(0, center_y - half_subgrid_size)
    end_row = min(grid_height, center_y + half_subgrid_size + 1)
    start_col = max(0, center_x - half_subgrid_size)
    end_col = min(grid_width, center_x + half_subgrid_size + 1)

    # Adjust the start and end indices to always print a subgrid of fixed size
    # Handle edge cases where the current point is near the boundaries
    if end_row - start_row < subgrid_size:
        if start_row == 0:
            end_row = min(subgrid_size, grid_height)
        elif end_row == grid_height:
            start_row = max(0, grid_height - subgrid_size)

    if end_col - start_col < subgrid_size:
        if start_col == 0:
            end_col = min(subgrid_size, grid_width)
        elif end_col == grid_width:
            start_col = max(0, grid_width - subgrid_size)

    for i in range(start_row, end_row):
        for j in range(start_col, end_col):
            curr_pos = Point(j, i, grid)
            if PATH_DEQUE and curr_pos in PATH_DEQUE:
                color_idx = PATH_DEQUE.index(curr_pos)
                color = COLORS[color_idx]
                console.print(f" {grid[i][j]} ", style=f"color({color})", end="")
            else:
                console.print(f" {grid[i][j]} ", style="none", end="")  # Print existing grid value
        print()  # New line at the end of each row


class Direction(Enum):
    UP = Point(0, -1)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)


PIPE_MAP = {
    "F": {Direction.DOWN: ["|", "L", "J"], Direction.RIGHT: ["-", "J", "7"]},
    "|": {Direction.DOWN: ["|", "L", "J"], Direction.UP: ["|", "7", "F"]},
    "7": {Direction.DOWN: ["|", "L", "J"], Direction.LEFT: ["-", "F", "L"]},
    "J": {Direction.UP: ["|", "7", "F"], Direction.LEFT: ["-", "F", "L"]},
    "L": {Direction.UP: ["|", "7", "F"], Direction.RIGHT: ["-", "J", "7"]},
    "-": {Direction.LEFT: ["-", "F", "L"], Direction.RIGHT: ["-", "7", "J"]},
}


def get_data(test: bool = TEST):
    input_file = get_input_file(test)
    data = input_file.read_text()
    return data


def get_input_file(test: bool = TEST):
    input_file = curr_dir / TEST_INPUT_FILE if test else curr_dir / "input"
    return input_file


def line_to_numbers(line: str):
    numbers = list(map(int, line.split()))
    return numbers


def line_to_list(line: str):
    return list(line)


def get_start_position(lines: list[str]) -> Point:
    for i, line in enumerate(lines):
        if "S" in line:
            return Point(line.index("S"), i, lines)


def get_opposite_direction(direction: Direction):
    if direction == Direction.UP:
        return Direction.DOWN
    if direction == Direction.DOWN:
        return Direction.UP
    if direction == Direction.LEFT:
        return Direction.RIGHT
    if direction == Direction.RIGHT:
        return Direction.LEFT
    return None


def get_offset_char(lines: list[str], pos: Point, direction: Direction):
    offset_point = pos.get_offset_point(direction)
    if offset_point.x < 0:
        return "."
    try:
        offset_char = lines[offset_point.y][offset_point.x]
        return offset_char
    except IndexError:
        return "."


def can_proceed(lines: list[str], pos: Point, direction: Direction):
    offset_char = get_offset_char(lines, pos, direction)
    if offset_char == ".":
        return False

    pipe_map = PIPE_MAP[pos.char] if pos.char != "S" else PIPE_MAP[S]
    if offset_char in pipe_map.get(direction, []):
        return True

    return False


# def navigate(
#     lines: list[str],
#     pos: Point,
#     pos_list: list[Point],
#     graph: Graph,
#     prev_direction: Direction = None,
# ):
#     pos_list.append(pos)

#     potential_directions = []
#     for direction in Direction:
#         if can_proceed(lines, pos, direction):
#             if direction == get_opposite_direction(prev_direction):
#                 continue
#             potential_directions.append(direction)

#     if len(potential_directions) == 0 or len(potential_directions) > 1:
#         raise Exception("Invalid number of directions")

#     direction = potential_directions[0]
#     offset_point = pos.get_offset_point(direction)
#     if graph.has_edge(pos, offset_point) or graph.has_edge(offset_point, pos):
#         raise Exception("Cycle detected")
#     graph.add_edge(pos, offset_point)
#     distance_ = distance_from_origin(offset_point.x, offset_point.y)
#     print(distance_)
#     # pos.print_point_and_next_point_on_grid(direction.value)

#     navigate(lines, offset_point, pos_list, graph, direction)

#     return pos_list


def iterative_navigate(grid: list[list[str]], start_point: Point, prev_direction: Direction = None):
    stack = [(start_point, 0, prev_direction)]  # Stack holds tuples of (Point, distance)
    visited = {}  # Dictionary to hold visited points and their distances
    max_distance = 0

    while stack:
        current_point, current_distance, prev_direction = stack.pop()

        # Skip if we've visited this point with a shorter or equal path
        if current_point in visited and current_distance <= visited[current_point]:
            continue

        # Update visited with the current distance
        visited[current_point] = current_distance
        max_distance = max(max_distance, current_distance)

        # Check and add adjacent points to the stack
        for direction in Direction:
            if can_proceed(grid, current_point, direction) and direction != get_opposite_direction(prev_direction):
                next_point = current_point.get_offset_point(direction)
                stack.append((next_point, current_distance + 1, direction))

    return max_distance, visited


def distance_from_origin(x, y):
    return math.sqrt(x**2 + y**2)


def main():
    lines = get_data().splitlines()
    lines = list(map(line_to_list, lines))
    start_pos = get_start_position(lines)

    max_distance, visited = iterative_navigate(lines, start_pos)
    print(max_distance)
    print(max_distance / 2)
    print(len(visited) // 2)


main()
