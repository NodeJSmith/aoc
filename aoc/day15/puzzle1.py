from pathlib import Path

from aoc_utils import get_data, line_to_list

TEST = False

"""
Determine the ASCII code for the current character of the string.
Increase the current value by the ASCII code you just determined.
Set the current value to itself multiplied by 17.
Set the current value to the remainder of dividing itself by 256.
"""


def line_hash(line: list[str]):
    curr_val = 0
    for char in line:
        curr_val += ord(char)
        curr_val *= 17
        curr_val %= 256
    return curr_val


def list_of_lists_to_tuples(lines: list[list[str]]):
    return tuple(map(tuple, lines))


def tuple_of_tuples_to_lists(lines: tuple[tuple[str, ...], ...]):
    return list(map(list, lines))


def get_line_dict(data):
    line_dict: dict[str, list[int]] = {}

    for line in data:
        pattern, hint = line.split(" ")
        line_dict[pattern] = list(map(int, hint.split(",")))

    return line_dict


def flip_rows_to_cols(lines: list[list[str]]):
    new_lines = []
    for col in range(len(lines[0])):
        new_line = []
        for row in range(len(lines)):
            new_line.append(lines[row][col])
        new_lines.append(new_line)
    return new_lines


def main():
    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, TEST)
    data = data.split(",")
    lines = list(map(line_to_list, data))

    total_val = 0
    for line in lines:
        line = [x for x in line if x != "\n"]
        total_val += line_hash(line)

    print(total_val)


main()
