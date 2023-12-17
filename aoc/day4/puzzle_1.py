from pathlib import Path

TEST = False

curr_dir = Path(__file__).parent


def get_data(test: bool = TEST):
    input_file = curr_dir / "test_input.txt" if test else curr_dir / "input.txt"
    data = input_file.read_text().splitlines()
    return data


def transform_data(data):
    cards = {}

    for line in data:
        # all whitespace to single space
        line = " ".join(line.split())
        card, card_data = line.split(":")

        card_data = card_data.strip().split(" | ")
        card_dict = {}

        # Creating the card dictionary
        card_dict["desired_numbers"] = set(map(int, card_data[0].split()))
        card_dict["actual_numbers"] = set(map(int, card_data[1].split()))

        cards[card] = card_dict

    return cards


def get_winning_numbers(cards: dict[str, dict[str, set]]):
    for _, card_data in cards.items():
        card_data["winning_numbers"] = card_data["desired_numbers"].intersection(card_data["actual_numbers"])

    return cards


output_data = get_winning_numbers(transform_data(get_data()))

output_dict: dict[str, int] = {}
for k, v in output_data.items():
    num_winners = len(v["winning_numbers"])
    base = 0
    for i in range(num_winners):
        if i == 0:
            base = 1
            continue
        base = base * 2

    if base:
        output_dict[k] = base

for k, v in output_dict.items():
    print(k, v)

print(sum(output_dict.values()))
