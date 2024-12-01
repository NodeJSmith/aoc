from pathlib import Path

curr_dir = Path(__file__).parent
input_file = curr_dir / "input.txt"

with open(input_file, "r") as f:
    lines = f.readlines()


# loop through lines and keep only digits from each line, do not change the order
digit_lines = []
for line in lines:
    digit_line = [str(digit) for digit in line if digit.isdigit()]
    digit_lines.append(digit_line)

# loop through digit_lines and sum first and last value
calibration_values = []

for line in digit_lines:
    first = line[0]
    last = line[-1]
    calibration_values.append(f"{first}{last}")

total_calibration_value = sum(map(int, calibration_values))

print(total_calibration_value)
