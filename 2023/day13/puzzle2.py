from copy import deepcopy
from pathlib import Path

from aoc_utils import get_data, line_to_list
from Levenshtein import distance

TEST = False


def get_groups(lines: list[list[str]]):
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


def list_of_lists_to_tuples(lines: list[list[str]]):
    return tuple(map(tuple, lines))


def tuple_of_tuples_to_lists(lines: tuple[tuple[str, ...], ...]):
    return list(map(list, lines))


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
    even_len = actual_len - 1 if actual_len % 2 != 0 else actual_len

    for i in range(2):
        first_half_tuple = (i, (even_len // 2) + i)
        second_half_tuple = ((even_len // 2) + i, even_len + i)
        first_half = lines[first_half_tuple[0] : first_half_tuple[1]]

        second_half = lines[second_half_tuple[0] : second_half_tuple[1]]

        if first_half == list(reversed(second_half)):
            return first_half_tuple[1]
    return None


class SmudgeChecker:
    def __init__(self, lines):
        self.smudge_fixed = False
        self.orig_lines = deepcopy(lines)
        self.lines = lines

    def get_fresh_lines(self):
        return deepcopy(self.orig_lines)

    def try_again(self):
        self.lines = self.get_fresh_lines()
        self.smudge_fixed = False
        return self.find_reflection()

    def check_outward(self, first_idx, second_idx):
        while True:
            first_idx -= 1
            second_idx += 1
            if first_idx < 0 or second_idx > len(self.lines):
                break
            try:
                s1 = self.lines[first_idx]
                s2 = self.lines[second_idx]
                lev_distance = distance(s1, s2)
                if lev_distance == 1 and not self.smudge_fixed:
                    # print(f"Smudge found at {first_idx}, {second_idx} (check_outward)")
                    s1, s2 = self.fix_smudge(first_idx, second_idx)
                if s1 != s2:
                    return False
            except IndexError:
                break
        return self.smudge_fixed

    def fix_smudge(self, i, j):
        assert not self.smudge_fixed

        s1 = deepcopy(self.lines[i])
        s2 = deepcopy(self.lines[j])
        for idx in range(len(s1)):
            if s1[idx] != s2[idx]:
                s1[idx] = s2[idx]
                break

        self.smudge_fixed = True

        return s1, s2

    def get_min_distance(self):
        distances = []
        distance_map = {}
        fresh_lines = self.get_fresh_lines()
        for i in range(len(fresh_lines)):
            for j in range(len(fresh_lines)):
                if i == j:
                    continue
                curr_distance = distance(fresh_lines[i], fresh_lines[j])
                distances.append(curr_distance)
                distance_map[(i, j)] = curr_distance

        min_distance = 0 if not distances else min(distances)

        # print(min_distance)
        return min_distance

    def find_reflection(self):
        self.get_min_distance()
        for i in range(len(self.lines) - 1):
            self.smudge_fixed = False
            s1 = self.lines[i]
            s2 = self.lines[i + 1]

            lev_distance = distance(s1, s2)
            if lev_distance == 1 and not self.smudge_fixed:
                # print(f"Smudge found at {i}, {i + 1} (find_reflection)")
                s1, s2 = self.fix_smudge(i, i + 1)
            if s1 == s2:
                if self.check_outward(i, i + 1):
                    return i + 1
        return None


def main():
    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, TEST).splitlines()
    lines = list(map(line_to_list, data))

    groups = get_groups(lines)

    total = 0
    for i, group in enumerate(groups):
        sc = SmudgeChecker(group)
        result = sc.find_reflection()
        if result and sc.smudge_fixed:
            total += 100 * result
            continue

        sc_flipped = SmudgeChecker(flip_rows_to_cols(group))
        result = sc_flipped.find_reflection()
        if result and sc_flipped.smudge_fixed:
            total += result
            continue

        print(f"No reflection found for group {i}")

    return total


total = main()

print(total)
