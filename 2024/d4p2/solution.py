from pathlib import Path

import attrs
from rich.console import Console

from aoc_helper import AocData, Grid

CONSOLE = Console()

AOC_DATA = AocData(Path(__file__).resolve().parent)

AOC_DATA.print(f"Day {AOC_DATA.day} Part {AOC_DATA.part}")
AOC_DATA.print(f"Test Mode: {'Yes' if AOC_DATA.args.test else 'No'}")
FOUND_COORDS = set()


@attrs.define
class X_Shape:
    center_coord: tuple[int, int]
    top_left_coord: tuple[int, int]
    top_right_coord: tuple[int, int]
    bottom_left_coord: tuple[int, int]
    bottom_right_coord: tuple[int, int]
    grid: Grid

    def __attrs_post_init__(self):
        if not isinstance(self.grid, Grid):
            self.grid = Grid(self.grid)

    @property
    def all_coords(self) -> set[tuple[int, int]]:
        return {
            self.center_coord,
            self.top_left_coord,
            self.top_right_coord,
            self.bottom_left_coord,
            self.bottom_right_coord,
        }

    @property
    def top_left_char(self):
        return self.grid[self.top_left_coord[0]][self.top_left_coord[1]]

    @property
    def top_right_char(self):
        return self.grid[self.top_right_coord[0]][self.top_right_coord[1]]

    @property
    def bottom_left_char(self):
        return self.grid[self.bottom_left_coord[0]][self.bottom_left_coord[1]]

    @property
    def bottom_right_char(self):
        return self.grid[self.bottom_right_coord[0]][self.bottom_right_coord[1]]

    @property
    def center_char(self):
        return self.grid[self.center_coord[0]][self.center_coord[1]]

    @property
    def first_part_str(self):
        return f"{self.top_left_char}{self.center_char}{self.bottom_right_char}"

    @property
    def second_part_str(self):
        return f"{self.top_right_char}{self.center_char}{self.bottom_left_char}"

    @property
    def is_match(self):
        if self.center_char != "A":
            return False

        if self.grid.any_out_of_bounds(self.all_coords):
            return False

        first_part = False
        second_part = False

        if self.first_part_str == "MAS" or self.first_part_str == "SAM":
            first_part = True

        if self.second_part_str == "MAS" or self.second_part_str == "SAM":
            second_part = True

        return first_part and second_part

    def pretty_print(self):
        AOC_DATA.print(self.center_coord)
        new_grid = self.grid.highlight_coords(coords=self.all_coords, highlight_style="bold red")

        return new_grid.get_section_as_str_from_origin(self.center_coord, 3, 3)


GRID = Grid([list(x) for x in AOC_DATA.data.splitlines()])

pos_a = GRID.get_coords_of_char("A")

num_found = 0
for coord in pos_a:
    item = X_Shape(
        center_coord=coord,
        top_left_coord=(coord[0] - 1, coord[1] - 1),
        top_right_coord=(coord[0] - 1, coord[1] + 1),
        bottom_left_coord=(coord[0] + 1, coord[1] - 1),
        bottom_right_coord=(coord[0] + 1, coord[1] + 1),
        grid=GRID,
    )
    if item.is_match:
        num_found += 1
        if any(not item.grid.in_bounds(*coord) for coord in item.all_coords):
            AOC_DATA.print()
            AOC_DATA.print(item.pretty_print())
            AOC_DATA.print()

AOC_DATA.force_print(num_found)
