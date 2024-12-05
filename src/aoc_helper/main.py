import argparse
import re
from functools import wraps
from pathlib import Path
from typing import Literal

import attrs
from rich.console import Console

DAY_PART_PATTERN = re.compile(r"d(\d+)p(\d+)")


@attrs.define
class Args:
    test: bool
    force_print: bool


@attrs.define
class AocData:
    curr_dir: Path
    args: Args = attrs.field(init=False)
    console: Console = attrs.field(init=False)

    def __attrs_post_init__(self):
        parser = argparse.ArgumentParser(description=f"Day {self.day} Part {self.part}")
        parser.add_argument("--test", "-t", help="Use the test input", action="store_true")
        parser.add_argument(
            "--force-print", "--fp", help="Print the data when not running in test mode", action="store_true"
        )

        args = parser.parse_args()
        self.args = Args(test=args.test, force_print=args.force_print)
        self.console = Console()

    @property
    def day(self):
        return int(DAY_PART_PATTERN.match(self.curr_dir.name).group(1))

    @property
    def part(self):
        return int(DAY_PART_PATTERN.match(self.curr_dir.name).group(2))

    @property
    def input_file(self):
        return self.curr_dir / ("input" if not self.args.test else "test_input")

    @property
    def data(self):
        return self.input_file.read_text()

    @wraps(Console.print)
    def print(self, *args, **kwargs):
        if self.args.force_print or self.args.test:
            self.console.print(*args, **kwargs)

    @wraps(Console.print)
    def force_print(self, *args, **kwargs):
        self.console.print(*args, **kwargs)


@attrs.define
class Grid:
    data: list[list[str]]

    @property
    def rows(self):
        if not self.data:
            return 0
        return len(self.data)

    @property
    def cols(self):
        if not self.data:
            return 0
        return len(self.data[0])

    def in_bounds(self, row: int, col: int):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def out_of_bounds(self, row: int, col: int):
        return not self.in_bounds(row, col)

    def all_in_bounds(self, coords: set[tuple[int, int]]):
        return all(self.in_bounds(row, col) for row, col in coords)

    def any_out_of_bounds(self, coords: set[tuple[int, int]]):
        return any(self.out_of_bounds(row, col) for row, col in coords)

    def get(self, row: int, col: int):
        if self.in_bounds(row, col):
            return self.data[row][col]
        return None

    def get_as_str(self) -> str:
        return "\n".join(["".join(row) for row in self.data])

    def get_section_as_str(
        self,
        start_row: int,
        start_col: int,
        end_row: int,
        end_col: int,
        join_char=" ",
        if_out_of_bounds: Literal["raise", "truncate"] = "truncate",
    ) -> str:
        rows = []
        if not self.in_bounds(start_row, start_col) or not self.in_bounds(end_row, end_col):
            if if_out_of_bounds == "raise":
                raise ValueError("Out of bounds")
            if if_out_of_bounds == "truncate":
                start_row = max(start_row, 0)
                start_col = max(start_col, 0)
                end_row = min(end_row, self.rows)
                end_col = min(end_col, self.cols)

        for row in range(start_row, min(end_row, self.rows)):
            rows.append(join_char.join(self.data[row][start_col:end_col]))

        return "\n".join(rows)

    def get_section_as_str_from_origin(
        self, origin: tuple[int, int], num_rows: int, num_cols: int, join_char=" "
    ) -> str:
        start_row = origin[0] - num_rows
        start_col = origin[1] - num_cols
        end_row = origin[0] + num_rows
        end_col = origin[1] + num_cols
        return self.get_section_as_str(start_row, start_col, end_row, end_col, join_char)

    def get_grid_subsection(self, start_row: int, start_col: int, num_rows: int, num_cols: int) -> "Grid":
        end_row = start_row + num_rows
        end_col = start_col + num_cols
        return Grid([list(row[start_col:end_col]) for row in self.data[start_row:end_row]])

    def get_grid_subsection_from_origin(self, origin: tuple[int, int], num_rows: int, num_cols: int) -> "Grid":
        start_row = origin[0] - num_rows
        start_col = origin[1] - num_cols
        return self.get_grid_subsection(start_row, start_col, num_rows, num_cols)

    def highlight_coords(self, coords: set[tuple[int, int]], highlight_style="bold red") -> "Grid":
        new_data = [list(row) for row in self.data]
        for row, col in coords:
            new_data[row][col] = f"[{highlight_style}]{new_data[row][col]}[/{highlight_style}]"
        return Grid(new_data)

    def get_coords_of_char(self, char: str) -> set[tuple[int, int]]:
        return {(row, col) for row, row_data in enumerate(self.data) for col, c in enumerate(row_data) if c == char}

    def __getitem__(self, key):
        return self.data[key]
