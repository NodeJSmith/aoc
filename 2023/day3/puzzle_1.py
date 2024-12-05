from pathlib import Path

TEST = False

curr_dir = Path(__file__).parent

expected_test_output = curr_dir / "expected_output.txt"
test_input_file = curr_dir / "test_input.txt"
input_file = curr_dir / "input.txt"

test_data = test_input_file.read_text().splitlines()
real_data = input_file.read_text().splitlines()

data = test_data if TEST else real_data


offsets = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
num_starts_grid: set[tuple[int, int]] = set()

for i, line in enumerate(data):
    for j, letter in enumerate(line):
        if letter.isalnum() or letter == ".":
            continue

        for offset in offsets:
            grid_point = (i + offset[0], j + offset[1])
            offset_val: str = data[grid_point[0]][grid_point[1]]
            if offset_val.isdigit():
                num_starts_grid.add(grid_point)


part_numbers: dict[tuple[int, int], int] = {}

for grid_point in num_starts_grid:
    line = data[grid_point[0]]
    col_num = grid_point[1]
    while line[col_num].isdigit():
        col_num -= 1
    start_col_num = col_num

    col_num = grid_point[1]

    while col_num < len(line) and line[col_num].isdigit():
        col_num += 1
    end_col_num = col_num

    coordinates = (grid_point[0], start_col_num + 1, end_col_num)
    full_digit = line[start_col_num + 1 : end_col_num]
    part_numbers[coordinates] = int(full_digit)

part_numbers_sorted = dict(sorted(part_numbers.items(), key=lambda item: item[0]))

for k, v in part_numbers_sorted.items():
    print(k, v)

if TEST:
    print(sorted(list(map(int, expected_test_output.read_text().splitlines()))))


sum_my_output = sum(list(part_numbers_sorted.values()))
if TEST:
    sum_expected_output = sum(sorted(list(map(int, expected_test_output.read_text().splitlines()))))
    assert sum_my_output == sum_expected_output

print(sum_my_output)
