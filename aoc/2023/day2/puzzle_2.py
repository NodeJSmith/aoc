from collections import defaultdict
from pathlib import Path

curr_dir = Path(__file__).parent

test_input_file = curr_dir / "test_input.txt"
input_file = curr_dir / "input.txt"

test_data = test_input_file.read_text().splitlines()
data = input_file.read_text().splitlines()

COLORS = ["red", "green", "blue"]


game_counts = {}

for line in data:
    game_title, games = line.split(":")
    game_num = game_title.replace("Game ", "")
    iteration = games.split(";")
    min_cubes = defaultdict(set)

    for i in iteration:
        iteration_cubes = i.split(",")
        green_cubes = [c for c in iteration_cubes if "green" in c] or None
        red_cubes = [c for c in iteration_cubes if "red" in c] or None
        blue_cubes = [c for c in iteration_cubes if "blue" in c] or None

        if green_cubes:
            green_cubes = green_cubes[0].strip().replace("green", "")
            min_cubes["green"].add(int(green_cubes))

        if red_cubes:
            red_cubes = red_cubes[0].strip().replace("red", "")
            min_cubes["red"].add(int(red_cubes))

        if blue_cubes:
            blue_cubes = blue_cubes[0].strip().replace("blue", "")
            min_cubes["blue"].add(int(blue_cubes))

    game_counts[game_num] = min_cubes


game_powers: dict[str, int] = {}
for k, v in game_counts.items():
    power = max(v["red"]) * max(v["green"]) * max(v["blue"])
    game_powers[k] = power

sum_powers = sum(game_powers.values())

print(f"Sum of powers: {sum_powers}")
