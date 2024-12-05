from itertools import combinations
from pathlib import Path

from rich.console import Console

console = Console(highlight=False)
TEST = False
TEST_INPUT_FILE = "test_input"
curr_dir = Path(__file__).parent


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


def print_lines(lines: list[str] | list[list[str]]):
    if isinstance(lines[0], list):
        lines = ["".join(line) for line in lines]

    for line in lines:
        print(line)

    print()


def row_has_no_galaxy(lines: list[list[str]], row: int):
    return not any(char == "#" or char.isdigit() for char in lines[row])


def col_has_no_galaxy(lines: list[list[str]], col: int):
    return not any(line[col] == "#" or line[col].isdigit() for line in lines)


def get_rows_without_galaxy(lines: list[list[str]]):
    return [row for row in range(len(lines)) if row_has_no_galaxy(lines, row)]


def get_cols_without_galaxy(lines: list[list[str]]):
    return [col for col in range(len(lines[0])) if col_has_no_galaxy(lines, col)]


def insert_empty_row(lines: list[list[str]], row: int):
    lines.insert(row, ["x" for _ in range(len(lines[0]))])


def insert_empty_col(lines: list[list[str]], col: int):
    for line in lines:
        line.insert(col, "x")


def expand_galaxy(lines: list[list[str]]):
    cols = get_cols_without_galaxy(lines)
    rows = get_rows_without_galaxy(lines)

    return rows, cols


def adjust_distances(
    distances: dict[tuple[int, int], int],
    adj_rows: list[int],
    adj_cols: list[int],
    grid_points: dict[int, tuple[int, int]],
):
    """
      0 1 2 3 4 5 6 7 8 9
    0|. . x 1 . x . . x .
    1|. . x . . x . 2 x .
    2|3 . x . . x . . x .
    3|x x x x x x x x x x
    4|. . x . . x 4 . x .
    5|. 5 x . . x . . x .
    6|. . x . . x . . x 6
    7|x x x x x x x x x x
    8|. . x . . x . 7 x .
    9|8 . x . 9 x . . x .

    """

    multiplier = 1_000_000

    adj_distances = {}
    for combo, distance in distances.items():
        x1, y1 = grid_points[combo[0]]
        x2, y2 = grid_points[combo[1]]

        for i in adj_rows:
            if i >= min(y1, y2) and i <= max(y1, y2):
                distance += multiplier - 1

        for i in adj_cols:
            if i >= min(x1, x2) and i <= max(x1, x2):
                distance += multiplier - 1

        adj_distances[combo] = distance

    return adj_distances


def get_distances(grid_points: dict[int, tuple[int, int]]) -> dict[tuple[int, int], int]:
    combos = list(combinations(grid_points.keys(), 2))
    distances: dict[tuple[int, int], int] = {}

    for combo in combos:
        p1, p2 = combo
        x1, y1 = grid_points[p1]
        x2, y2 = grid_points[p2]

        distance = abs(x1 - x2) + abs(y1 - y2)
        distances[combo] = distance
    return distances


def main(lines: list[list[str]] | None = None):
    print_lines(lines)

    adj_rows, adj_cols = expand_galaxy(lines)

    grid_points: dict[int, tuple[int, int]] = {}
    count = 1
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                lines[i][j] = str(count)
                grid_points[count] = (j, i)
                count += 1

    print()
    print_lines(lines)

    distances = get_distances(grid_points)

    adj_distances = adjust_distances(distances, adj_rows, adj_cols, grid_points)

    print(sum(list(adj_distances.values())))

    return grid_points, adj_distances


if __name__ == "__main__":
    orig_lines = list(map(line_to_list, get_data().splitlines()))

    grid_points, distances = main(orig_lines)
