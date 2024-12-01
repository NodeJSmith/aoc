import sys
from copy import deepcopy
from enum import Enum
from pathlib import Path

import numpy as np
from rich.console import Console
from rich.text import Text

console = Console()


TEST_INPUT_FILE = "test_input"
INPUT_FILE = "input"


def point_in_bounds(point: tuple[int, int], arr: np.ndarray):
    row, col = point  # Assuming the point is given as (row, column)
    return 0 <= col < arr.shape[1] and 0 <= row < arr.shape[0]


def point_out_of_bounds(point: tuple[int, int], data: np.ndarray):
    return not point_in_bounds(point, data)


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
            elif (
                grid is not None
                and not point_out_of_bounds(point, grid)
                and grid[point] == 1
            ):
                output.append(value, style="bold blue")
            else:
                output.append(value)
        output.append("\n")

    console.print(output)


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


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


def print_char(
    curr_pos,
    lines,
    wide_mode: bool = False,
    highlights: dict[tuple[int, int], str] = None,
):
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

        col_line = [" "] + [
            f"{get_index_val(i)}" for i in range(len(copied_lines[0]) - 1)
        ]
        copied_lines.insert(0, col_line)

        adjusted_highlights = {}

        for k, v in highlights.items():
            adjusted_highlights[(k[0] + 1, k[1] + 1)] = v

    else:
        adjusted_highlights = highlights

    for row in range(0, len(copied_lines)):
        for col in range(0, len(copied_lines[0])):
            curr_pos = (col, row)
            print_char(
                curr_pos=curr_pos,
                lines=copied_lines,
                wide_mode=wide_mode,
                highlights=adjusted_highlights,
            )

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


def first_nonzero_row(arr: np.ndarray):
    # find smallest non-zero row
    smallest_row = 0
    for row in range(arr.shape[0]):
        if np.sum(arr[row, :]) > 0:
            smallest_row = row
            break
    return smallest_row


def first_nonzero_col(arr: np.ndarray):
    # find smallest non-zero column
    smallest_col = 0

    if len(arr.shape) == 1:
        for col in range(arr.shape[0]):
            if bool(arr[col]):
                smallest_col = col
                break
        return smallest_col

    for col in range(arr.shape[1]):
        if np.count_nonzero(arr[:, col]) > 0:
            smallest_col = col
            break
    return smallest_col


def last_nonzero_row(arr: np.ndarray):
    # find largest non-zero row
    largest_row = 0
    for row in range(arr.shape[0] - 1, 0, -1):
        if np.sum(arr[row, :]) > 0:
            largest_row = row
            break
    return largest_row


def last_nonzero_col(arr: np.ndarray):
    # find largest non-zero column
    largest_col = 0

    if len(arr.shape) == 1:
        for col in range(arr.shape[0] - 1, 0, -1):
            if arr[col] > 0:
                largest_col = col
                break
        return largest_col

    for col in range(arr.shape[1] - 1, 0, -1):
        if np.sum(arr[:, col]) > 0:
            largest_col = col
            break
    return largest_col
