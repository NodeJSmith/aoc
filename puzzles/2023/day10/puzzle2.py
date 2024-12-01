import math
import sys
from collections import deque
from enum import Enum
from pathlib import Path
from typing import Optional, Union

from PIL import Image, ImageDraw, ImageFont
from rich.console import Console

console = Console(highlight=False)
TEST = False
TEST_INPUT_FILE = "test_input4"
S = "|" if not TEST else "F"
if TEST_INPUT_FILE == "test_input3":
    S = "7"  # type: ignore
curr_dir = Path(__file__).parent
COLORS = range(125, 160)

PATH_DEQUE = deque(maxlen=4)
FONT_PATH = "/home/jessica/.local/share/fonts/ttf/FiraCode-Regular.ttf"
FILL_CHAR = " "


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

pipe_symbols = {
    "|": "\u2502",  # Box Drawings Light Vertical
    "-": "\u2500",  # Box Drawings Light Horizontal
    "L": "\u2514",  # Box Drawings Light Up and Right
    "J": "\u2518",  # Box Drawings Light Up and Left
    "7": "\u2510",  # Box Drawings Light Down and Left
    "F": "\u250C",  # Box Drawings Light Down and Right
    ".": ".",  # Ground
    "S": "★",  # Starting Position
}


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


old_pipe_map = {
    "F": {Direction.DOWN: ["|", "L", "J"], Direction.RIGHT: ["-", "J", "7"]},
    "|": {Direction.DOWN: ["|", "L", "J"], Direction.UP: ["|", "7", "F"]},
    "7": {Direction.DOWN: ["|", "L", "J"], Direction.LEFT: ["-", "F", "L"]},
    "J": {Direction.UP: ["|", "7", "F"], Direction.LEFT: ["-", "F", "L"]},
    "L": {Direction.UP: ["|", "7", "F"], Direction.RIGHT: ["-", "J", "7"]},
    "-": {Direction.LEFT: ["-", "F", "L"], Direction.RIGHT: ["-", "7", "J"]},
}
PIPE_MAP = {}
for k, v in old_pipe_map.items():
    new_char = pipe_symbols[k]
    PIPE_MAP[new_char] = {}
    for direction, chars in v.items():
        PIPE_MAP[new_char][direction] = list(map(pipe_symbols.get, chars))


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


def map_to_unicode(grid: list[list[str]]):
    return [[pipe_symbols[char] for char in line] for line in grid]


def line_to_list(line: str):
    return list(line)


def get_start_position(lines: list[str]) -> Point:
    for i, line in enumerate(lines):
        if "★" in line:
            return Point(line.index("★"), i, lines)


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

    pipe_map = PIPE_MAP[pos.char] if pos.char != "★" else PIPE_MAP[pipe_symbols[S]]
    if offset_char in pipe_map.get(direction, []):
        return True

    return False


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

    return visited


def distance_from_origin(x, y):
    return math.sqrt(x**2 + y**2)


def flood_fill(grid, x, y, loop_points, fill_char=FILL_CHAR):
    if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid) or Point(x, y) in loop_points or grid[y][x] == fill_char:
        return

    grid[y][x] = fill_char

    flood_fill(grid, x + 1, y, loop_points, fill_char)
    flood_fill(grid, x - 1, y, loop_points, fill_char)
    flood_fill(grid, x, y + 1, loop_points, fill_char)
    flood_fill(grid, x, y - 1, loop_points, fill_char)


def perform_flood_fill_from_edges(grid, loop_points):
    grid_height = len(grid)
    grid_width = len(grid[0]) if grid_height > 0 else 0

    # Flood fill from each edge
    for x in range(grid_width):
        if grid[0][x] not in loop_points:  # Top edge
            flood_fill(grid, x, 0, loop_points)
        if grid[grid_height - 1][x] not in loop_points:  # Bottom edge
            flood_fill(grid, x, grid_height - 1, loop_points)

    for y in range(grid_height):
        if grid[y][0] not in loop_points:  # Left edge
            flood_fill(grid, 0, y, loop_points)
        if grid[y][grid_width - 1] not in loop_points:  # Right edge
            flood_fill(grid, grid_width - 1, y, loop_points)


def print_grid(lines):
    for line in lines:
        for char in line:
            if char == FILL_CHAR:
                console.print(char, style="blue", end="")
            elif char == "*":
                console.print(char, style="red", end="")
            elif char == "~":
                console.print(char, style="yellow1", end="")
            else:
                print(char, end="")
        print()


def create_image_from_grid_with_text(grid, tile_size=10, font_path=FONT_PATH):
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Create a new image with white background
    img = Image.new("RGB", (width * tile_size, height * tile_size), color="white")
    draw = ImageDraw.Draw(img)

    # Load a monospaced font
    try:
        font = ImageFont.truetype(font_path, tile_size)
    except IOError:
        font = ImageFont.load_default()

    # Define colors for each type of tile
    colors = {
        ".": "black",  # ground
        "*": "black",  # visited
        "o": "blue",  # flood fill
        "█": "red",  # enclosed
        # Add more colors for other characters if needed
    }

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "★":
                char = pipe_symbols[S]
            if char == pipe_symbols["-"]:
                char = char * 2
            elif char == pipe_symbols["F"]:
                char = char + pipe_symbols["-"]
            elif char == pipe_symbols["L"]:
                char = char + pipe_symbols["-"]
            elif char == "~":
                char = "█"

            color = colors.get(char, "black")  # Default to black
            draw.text((j * tile_size, i * tile_size), char, font=font, fill=color, align="center")

    return img


def detect_enclosed_tiles(image_path, grid, tile_size=10, enclosed_color=(255, 0, 0)):  # Red for enclosed
    img = Image.open(image_path).convert("RGB")

    all_colors = img.getcolors()

    for color in all_colors:
        color_str = "rgb(" + ",".join(map(str, color[1])) + ")"
        console.print("█", style=color_str, end="  ")
        print(color[1])

    enclosed_tiles = []

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "~":  # Check only potential enclosed tiles
                # Check the color of the central pixel in the tile
                center_pixel = (x * tile_size + tile_size // 2, y * tile_size + tile_size // 2)
                color = img.getpixel(center_pixel)
                color_str = "rgb(" + ",".join(map(str, color)) + ")"
                console.print(char, style=color_str)
                if color[0] == 255:
                    enclosed_tiles.append((x, y))

    return enclosed_tiles


def main():
    lines = get_data().splitlines()
    lines = list(map(line_to_list, lines))
    lines = map_to_unicode(lines)
    start_pos = get_start_position(lines)

    visited = iterative_navigate(lines, start_pos)

    # print_grid(lines)

    # for v in visited:
    #     lines[v[1]][v[0]] = "*"

    perform_flood_fill_from_edges(lines, visited)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if Point(x, y) not in visited and char != FILL_CHAR:
                lines[y][x] = "~"

    # print_grid(lines)

    tildes = 0

    for line in lines:
        for char in line:
            if char == "~":
                tildes += 1

    answer = tildes
    return lines, answer


sys.setrecursionlimit(100000)
lines, answer = main()

print("Key:")
console.print("[blue]o[/blue]: Flood fill")
console.print("[red]*[/red]: Visited")
console.print("[yellow]~[/yellow]: Enclosed")
incorrect_answers = [843, 769, 834]
if answer in incorrect_answers:
    print(f"Answer {answer} is incorrect")
else:
    print(answer)


# have to save the grid to a file, then open in a paint tool, fill it, then read the image back in
# TODO: automate this process (obviously)
# print_grid(lines)
# img = create_image_from_grid_with_text(lines)
# img.save("grid_output.png")

img_path = "./aoc/day10/grid_output.png"

tiles = detect_enclosed_tiles(img_path, lines)

print(len(tiles))
