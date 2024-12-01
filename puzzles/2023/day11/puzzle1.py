import pickle
from itertools import combinations
from pathlib import Path

from rich.console import Console

console = Console(highlight=False)
TEST = True
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
    return not any([char == "#" or char.isdigit() for char in lines[row]])


def col_has_no_galaxy(lines: list[list[str]], col: int):
    return not any([line[col] == "#" or line[col].isdigit() for line in lines])


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
    cols_without_galaxy = get_cols_without_galaxy(lines)
    rows_without_galaxy = get_rows_without_galaxy(lines)

    # adjusted_cols = [col + i for i, col in enumerate(cols_without_galaxy)]
    # adjusted_rows = [row + i for i, row in enumerate(rows_without_galaxy)]

    for i, col in enumerate(cols_without_galaxy):
        col += i
        insert_empty_col(lines, col)

    for i, row in enumerate(rows_without_galaxy):
        row += i
        insert_empty_row(lines, row)

    print_lines(lines)

    # return adjusted_rows, adjusted_cols


def adjust_points(points: dict[int, tuple[int, int]], rows: list[int], cols: list[int]):
    multiplier = 1
    new_points = {}
    for i, (x, y) in points.items():
        if x in rows:
            x += rows.index(x) * multiplier
        if y in cols:
            y += cols.index(y) * multiplier

        new_points[i] = (x, y)

    return new_points


def main(lines: list[list[str]] = None):
    print_lines(lines)

    # expand_galaxy(lines)

    grid_points: dict[int, tuple[int, int]] = {}
    count = 1
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                lines[i][j] = str(count)
                grid_points[count] = (i, j)
                count += 1

    print()
    print_lines(lines)

    numbers = list(range(1, count))
    combos = list(combinations(numbers, 2))
    distances: dict[tuple[int, int], int] = {}

    for combo in combos:
        p1, p2 = combo
        x1, y1 = grid_points[p1]
        x2, y2 = grid_points[p2]

        distance = abs(x1 - x2) + abs(y1 - y2)
        distances[combo] = distance

    print(sum(list(distances.values())))

    return grid_points, distances


if __name__ == "__main__":
    orig_lines = list(map(line_to_list, get_data().splitlines()))
    grid_points, distances = main(orig_lines)

    pickle.dump(grid_points, open("unexpanded_grid_points.pkl", "wb"))
    pickle.dump(distances, open("unexpanded_distances.pkl", "wb"))
