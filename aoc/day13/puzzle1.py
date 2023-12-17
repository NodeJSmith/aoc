from collections import Counter
from copy import deepcopy
from pathlib import Path

from aoc_utils import get_data, line_to_list

TEST = False


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


def find_reflection_simple(lines):
    lines = deepcopy(lines)

    actual_len = len(lines)
    if actual_len % 2 != 0:
        even_len = actual_len - 1
    else:
        even_len = actual_len

    for i in range(2):
        first_half_tuple = (i, (even_len // 2) + i)
        second_half_tuple = ((even_len // 2) + i, even_len + i)
        first_half = lines[first_half_tuple[0] : first_half_tuple[1]]

        second_half = lines[second_half_tuple[0] : second_half_tuple[1]]

        if first_half == list(reversed(second_half)):
            return first_half_tuple[1]


def check_outward(lines, first_idx, second_idx):
    while True:
        first_idx -= 1
        second_idx += 1
        if first_idx < 0 or second_idx >= len(lines):
            break
        try:
            if lines[first_idx] != lines[second_idx]:
                return False
        except IndexError:
            break
    return True


def find_reflection(lines):
    lines = list_of_lists_to_tuples(lines)

    line_counts = Counter(lines)

    repeated_lines = [line for line, count in line_counts.items() if count > 1]

    if not repeated_lines:
        return False

    for i in range(len(lines) - 1):
        if lines[i] not in repeated_lines:
            continue
        if lines[i] == lines[i + 1]:
            if check_outward(lines, i, i + 1):
                return i + 1


def get_groups(lines):
    groups = []

    curr_group = []
    while lines:
        curr_line = lines.pop(0)
        if curr_line:
            curr_group.append(curr_line)
        else:
            groups.append(curr_group)
            curr_group = []

    if curr_group:
        groups.append(curr_group)

    return groups


def main():
    answers = []

    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, TEST).splitlines()
    lines = list(map(line_to_list, data))

    groups = get_groups(lines)

    total = 0
    for i, group in enumerate(groups):
        result = find_reflection(group)
        if result:
            answers.append((i, result, "standard"))

            # group.insert(result, ["|"] * len(group[0]))
            # print_lines(group)

            total += 100 * result
            continue

        group = flip_rows_to_cols(group)
        result = find_reflection(group)

        if result:
            answers.append((i, result, "flipped"))
            # group.insert(result, ["|"] * len(group[0]))
            # print_lines(group)

            total += result
            continue

        print(f"No reflection found for group {i}")

    # with open(curr_dir / "answers.pkl", "wb") as f:
    #     pickle.dump(answers, f)

    return total


total = main()

print(total)


too_low_answers = [31861, 631]

if not TEST and (total in too_low_answers or total < max(too_low_answers)):
    raise Exception("Too low")
