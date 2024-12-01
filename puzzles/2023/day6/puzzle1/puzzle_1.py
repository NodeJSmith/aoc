import operator
from functools import reduce  # Valid in Python 2.6+, required in Python 3
from pathlib import Path

from tqdm import tqdm

TEST = False
curr_dir = Path(__file__).parent


def get_data(test: bool = TEST):
    input_file = get_input_file(test)
    data = input_file.read_text()
    return data


def get_input_file(test: bool = TEST):
    input_file = curr_dir / "test_input" if test else curr_dir / "input"
    return input_file


data = get_data()

groups = data.splitlines()

allowed_time = int("".join(groups[0].split()[1:]))
distance_record = int("".join(groups[1].split()[1:]))

races = {}


races["Race 1"] = {"allowed_time": allowed_time, "distance_record": distance_record}


for race, race_data in races.items():
    distance_record = race_data["distance_record"]
    allowed_time = race_data["allowed_time"]

    winning_combos = []
    for i in tqdm(range(allowed_time)):
        hold_time = i
        race_time = allowed_time - i
        distance = race_time * hold_time
        if distance > distance_record:
            winning_combos.append((hold_time, distance))

    races[race]["winning_combos"] = winning_combos

num_winning_combos = reduce(operator.mul, [len(r["winning_combos"]) for r in races.values()], 1)


print(num_winning_combos)


# this actually solves part 2, i seem to have overwritten the original part 1
