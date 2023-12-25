import sys
from copy import deepcopy
from enum import Enum
from pathlib import Path
from typing import Optional, Union

import numpy as np
from rich.console import Console
from rich.text import Text

console = Console()


TEST_INPUT_FILE = "test_input"
INPUT_FILE = "input"


def point_out_of_bounds(point: tuple[int, int], data: np.ndarray):
    return point[0] < 0 or point[1] < 0 or point[0] >= len(data[0]) or point[1] >= len(data)


def move_cursor_up(lines):
    sys.stdout.write(f"\033[{lines}A")


def print_colored_array(
    array: np.ndarray,
    grid: np.ndarray = None,
    colored_points: dict[tuple[int, int], str] = None,
    reset_cursor: bool = True,
):
    """
    Prints out a NumPy array with specific points colored.

    :param array: NumPy array to be printed.
    :param colored_points: Dictionary with points as keys (tuples of coordinates) and colors as values.
    """
    if reset_cursor:
        move_cursor_up(array.shape[0] + 1)

    output = Text()

    if not colored_points:
        colored_points = {}

    for y in range(array.shape[0]):
        for x in range(array.shape[1]):
            point = (y, x)
            value = str(array[y, x])
            if point in colored_points:
                output.append(value, style=f"bold {colored_points[point]}")
            elif grid is not None and not point_out_of_bounds(point, grid) and grid[point] == 1:
                output.append(value, style="bold blue")
            else:
                output.append(value)
        output.append("\n")

    console.print(output)


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


class Direction(Enum):
    UP = Point(0, -1)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)


def get_data(data_dir: str | Path, test: bool = False):
    input_file = get_input_file(data_dir, test)
    data = input_file.read_text()
    return data


def get_input_file(data_dir: str | Path, test: bool = False) -> Path:
    data_dir = Path(data_dir)
    input_file = data_dir / TEST_INPUT_FILE if test else data_dir / INPUT_FILE
    return Path(input_file)


def line_to_numbers(line: str):
    numbers = list(map(int, line.split()))
    return numbers


def line_to_list(line: str):
    return list(line)


def print_char(curr_pos, lines, wide_mode: bool = False, highlights: dict[tuple[int, int], str] = None):
    col, row = curr_pos

    if not highlights:
        highlights = {}

    if wide_mode:
        char = f" {lines[row][col]}"
    else:
        try:
            char = lines[row][col]
        except IndexError:
            return

    if highlights and curr_pos in highlights:
        color = highlights[curr_pos]
        console.print(f"{char}", style=color, end="")
    else:
        console.print(f"{char}", end="")  # Print existing grid value


def get_index_val(i):
    row_char = str(i)[0] if i < 10 else str(i)[-1]
    return row_char


def print_lines(
    lines: list[str] | list[list[str]],
    highlights: dict[tuple[int, int], str] = None,
    wide_mode: bool = False,
    add_line_break: bool = True,
    add_index: bool = False,
):
    copied_lines = deepcopy(lines)
    if isinstance(lines[0], str):
        copied_lines = list(map(line_to_list, copied_lines))

    if not highlights:
        highlights = {}

    if add_index:
        for row, line in enumerate(copied_lines):
            row_char = get_index_val(row)
            line.insert(0, f"{row_char}")  # type: ignore

        col_line = [" "] + [f"{get_index_val(i)}" for i in range(len(copied_lines[0]) - 1)]
        copied_lines.insert(0, col_line)

        adjusted_highlights = {}

        for k, v in highlights.items():
            adjusted_highlights[(k[0] + 1, k[1] + 1)] = v

    else:
        adjusted_highlights = highlights

    for row in range(0, len(copied_lines)):
        for col in range(0, len(copied_lines[0])):
            curr_pos = Point(col, row)
            print_char(curr_pos=curr_pos, lines=copied_lines, wide_mode=wide_mode, highlights=adjusted_highlights)

        print()  # New line at the end of each row

    if add_line_break:
        print()


def list_of_lists_to_tuples(lines: list[list[str]]):
    return tuple(map(tuple, lines))


def tuple_of_tuples_to_lists(lines: tuple[tuple[str, ...], ...]):
    return list(map(list, lines))


def flip_rows_to_cols(lines: list[list[str]]):
    new_lines = []
    for col in range(len(lines[0])):
        new_line = []
        for row in range(len(lines)):
            new_line.append(lines[row][col])
        new_lines.append(new_line)
    return new_lines
