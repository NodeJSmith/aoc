from pathlib import Path

from aoc_utils import get_data, line_to_list

TEST = False

BOXES = {i: [] for i in range(0, 256)}
FOCAL_LENGTHS = {}

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


def add_focusing_power(box_num, slot_num, focal_length):
    box_num = box_num + 1
    slot_num = slot_num + 1

    return box_num * slot_num * focal_length


def main():
    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, TEST)
    data = data.split(",")
    lines = list(map(line_to_list, data))

    total_val = 0
    for line in lines:
        line = [x for x in line if x != "\n"]
        if "-" in line:
            prehash = line[:-1]
            operation = line[-1]
        elif "=" in line:
            prehash = line[:-2]
            focal_length = line[-1]
            operation = "="

        prehash = "".join(prehash)
        hash_val = line_hash(prehash)

        if operation == "-":
            if prehash in BOXES[hash_val]:
                BOXES[hash_val].remove(prehash)
        elif operation == "=":
            if prehash not in BOXES[hash_val]:
                BOXES[hash_val].append(prehash)
                FOCAL_LENGTHS[prehash] = int(focal_length)
            else:
                FOCAL_LENGTHS[prehash] = int(focal_length)

    for box_num, box in enumerate(BOXES.values()):
        for slot_num, slot in enumerate(box):
            total_val += add_focusing_power(box_num, slot_num, FOCAL_LENGTHS[slot])

    print(total_val)


main()
