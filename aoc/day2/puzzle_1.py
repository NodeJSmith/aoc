from pathlib import Path

curr_dir = Path(__file__).parent

test_input_file = curr_dir / "test_input.txt"
input_file = curr_dir / "input.txt"

test_data = test_input_file.read_text().splitlines()
data = input_file.read_text().splitlines()

NUM_CUBES = {"red": 12, "green": 13, "blue": 14}

game_counts = {}

for line in data:
    game_title, games = line.split(":")
    game_num = game_title.replace("Game ", "")
    iteration = games.split(";")
    max_cubes = {k: 0 for k in NUM_CUBES.keys()}

    for i in iteration:
        iteration_cubes = i.split(",")
        green_cubes = [c for c in iteration_cubes if "green" in c] or None
        red_cubes = [c for c in iteration_cubes if "red" in c] or None
        blue_cubes = [c for c in iteration_cubes if "blue" in c] or None

        if green_cubes:
            green_cubes = green_cubes[0].strip().replace("green", "")
            if int(green_cubes) > max_cubes["green"]:
                max_cubes["green"] = int(green_cubes)

        if red_cubes:
            red_cubes = red_cubes[0].strip().replace("red", "")
            if int(red_cubes) > max_cubes["red"]:
                max_cubes["red"] = int(red_cubes)

        if blue_cubes:
            blue_cubes = blue_cubes[0].strip().replace("blue", "")
            if int(blue_cubes) > max_cubes["blue"]:
                max_cubes["blue"] = int(blue_cubes)

    game_counts[game_num] = max_cubes

impossible_games: set[str] = set()
possible_games: set[str] = set()

for k, v in game_counts.items():
    for color, max_count in NUM_CUBES.items():
        if v.get(color, 0) > max_count:
            impossible_games.add(k)
            break

    if k not in impossible_games:
        possible_games.add(k)


print(f"Impossible games: {impossible_games}")

print(f"Possible games: {possible_games}")


sum_poss_games = sum(list(map(int, possible_games)))

print(f"Sum of possible games: {sum_poss_games}")
