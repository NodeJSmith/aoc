from pathlib import Path

from aoc_utils import get_data, print_lines


def get_line_dict():
    line_dict: dict[str, list[int]] = {}

    for line in data:
        pattern, hint = line.split(" ")
        line_dict[pattern] = list(map(int, hint.split(",")))

    return line_dict


curr_dir = Path(__file__).parent.absolute()

data = get_data(curr_dir, True).splitlines()


def find_contiguous_string(line: str, start_idx: int, char: str):
    while line[start_idx] == char:
        start_idx += 1
    return start_idx


# line_dict = get_line_dict()

print_lines(data)

print(find_contiguous_string(data[0], 0, "?"))
