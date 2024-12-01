from collections import Counter
from pathlib import Path

import networkx
from networkx import Graph

TEST = False
OFFSETS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

INCORRECT_ANSWERS: dict[int, str] = {38_008_271: "Too Low", 51_355_246: "Too Low"}

curr_dir = Path(__file__).parent

expected_test_output = curr_dir / "expected_output.txt"
test_input_file = curr_dir / "test_input.txt"
input_file = curr_dir / "input.txt"

test_data = test_input_file.read_text().splitlines()
real_data = input_file.read_text().splitlines()
if TEST:
    data: list[str] = test_data
else:
    data: list[str] = real_data


def get_full_digit_coord(x: int, y: int) -> tuple[int, int, int, int]:
    line: str = data[x]
    col_num: int = y

    while line[col_num].isdigit():
        col_num -= 1
    start_col_num = col_num

    col_num = y

    while col_num < len(line) and line[col_num].isdigit():
        col_num += 1
    end_col_num = col_num

    x_point = slice(start_col_num + 1, end_col_num)
    full_digit = line[x_point]

    return (x, start_col_num + 1, end_col_num, int(full_digit))


def check_offset(x: int, y: int, x_offset: int, y_offset: int) -> tuple[int, int, int, int] | None:
    new_x = x + x_offset
    new_y = y + y_offset

    try:
        offset_val: str = data[new_x][new_y]
    except IndexError:
        return None

    if not offset_val.isdigit():
        return None

    coord = get_full_digit_coord(new_x, new_y)
    return coord


def add_edges(graph: networkx.Graph, x: int, y: int):
    coord = (x, y)
    if data[x][y] != "*":
        return

    for x_offset, y_offset in OFFSETS:
        full_coord = check_offset(x, y, x_offset, y_offset)
        if full_coord is None:
            continue
        graph.add_edge(coord, full_coord)


def get_gear_ratios(graph: networkx.Graph) -> list[int]:
    c = Counter([x[0] for x in list(graph.edges())])

    gears = [x for x in c if c[x] == 2 and isinstance(x, tuple)]

    gear_ratios: list[int] = []
    for g in gears:
        gear_vals = list(graph[g].keys())
        gear_ratio = int(gear_vals[0][-1]) * int(gear_vals[1][-1])
        gear_ratios.append(gear_ratio)
    return gear_ratios


def main():
    graph = Graph()

    for x, line in enumerate(data):
        for y, letter in enumerate(line):
            if letter.isalnum() or letter == ".":
                continue

            add_edges(graph, x, y)

    gear_ratios = get_gear_ratios(graph)

    answer = sum(gear_ratios)

    if answer in INCORRECT_ANSWERS:
        raise ValueError(f"Answer {answer} is incorrect. {INCORRECT_ANSWERS[answer]}")

    print(answer)


main()
