from pathlib import Path

TEST = False
curr_dir = Path(__file__).parent


def get_data(test: bool = TEST):
    input_file = get_input_file(test)
    data = input_file.read_text()
    return data


def get_input_file(test: bool = TEST):
    input_file = curr_dir / "test_input" if test else curr_dir / "input"
    return input_file


def line_to_numbers(line: str):
    numbers = list(map(int, line.split()))
    return numbers


def get_differences_lists(numbers: list, differences_list: list[list[int]] | None = None):
    differences_list: list[list[int]] = differences_list or [numbers]

    diffs = [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]
    differences_list.append(diffs)

    if not all([x == 0 for x in diffs]):
        get_differences_lists(diffs, differences_list)

    return differences_list


def get_next_number(numbers_lists: list[list[int]]):
    numbers_lists[-1].append(0)
    numbers_lists = list(reversed(numbers_lists))
    for i in range(len(numbers_lists) - 1):
        num_list = numbers_lists[i]
        next_num_list = numbers_lists[i + 1]
        num_a = num_list[-1]
        num_b = next_num_list[-1]
        print(f"{num_a} + {num_b}")
        diff = next_num_list[-1] + num_list[-1]
        next_num_list.append(diff)

    return numbers_lists[-1][-1]


lines = get_data().splitlines()
lines = list(map(line_to_numbers, lines))
print(lines)

final_nums: list[int] = []
for line in lines:
    output = get_differences_lists(line)
    next_num = get_next_number(output)
    final_nums.append(next_num)


answer = sum(final_nums)
print(answer)
