from pathlib import Path

DIGIT_STRINGS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

EXPECTED_TEST_RESULT = 281


def get_input_data(test: bool = False) -> list[tuple[str, str]]:
    curr_dir = Path(__file__).parent
    input_file = curr_dir / "test_input.txt" if test else curr_dir / "input.txt"

    new_lines: list[str] = []
    with open(input_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        for line in lines:
            orig_line = line
            new_line = replace_string_with_digit(line)

            if new_line != orig_line:
                print(f"replaced {orig_line:<15} with {new_line:<15}")
            new_lines.append(new_line)

    return list(zip(lines, new_lines))


def replace_string_with_digit(line: str) -> str:
    new_line = line

    i = 0
    while i < len(line):
        curr_value = line[i:]
        for digit_str, digit_int in DIGIT_STRINGS.items():
            if curr_value.lower().startswith(digit_str):
                # something like eightwo should be 82, so we have to include the -1 to account for potential overlap
                new_line = line[0:i] + str(digit_int) + line[i + len(digit_str) - 1 :]
                return replace_string_with_digit(new_line)
        i += 1

    return new_line


def get_digit_lines(lines: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    # loop through lines and keep only digits from each line, do not change the order

    digit_lines = []
    orig_lines = [line[0] for line in lines]
    adj_lines = [line[1] for line in lines]
    for line in adj_lines:
        digit_line = [str(digit) for digit in line if digit.isdigit()]
        digit_lines.append(digit_line)

    return list(zip(orig_lines, adj_lines, digit_lines))


def get_calibration_lines(lines: list[tuple[str, str, str]]) -> list[str]:
    # loop through digit_lines and sum first and last value
    calibration_values = []

    for original_line, adj_line, line in lines:
        first = line[0]
        last = line[-1]
        print(f"line:{original_line:<20} -> {adj_line:<15} -> {first}{last}")
        calibration_values.append(f"{first}{last}")

    return calibration_values


def main(test: bool = False):
    data = get_input_data(test)
    digit_lines = get_digit_lines(data)
    calibration_values = get_calibration_lines(digit_lines)

    total_calibration_value = sum(map(int, calibration_values))

    return total_calibration_value


if __name__ == "__main__":
    test_output = main(test=True)
    assert (
        test_output == EXPECTED_TEST_RESULT
    ), f"not expected result, expected: {EXPECTED_TEST_RESULT}, got: {test_output}"

    output = main()
    print(output)
