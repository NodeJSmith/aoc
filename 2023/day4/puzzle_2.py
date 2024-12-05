from collections import Counter
from copy import copy
from pathlib import Path

TEST = False

card_list: list["Card"] = []


class Card:
    number: int
    line: str
    desired_numbers: set[int]
    actual_numbers: set[int]
    winning_numbers: set[int]

    @classmethod
    def create(cls, line: str):
        card = cls(line)
        card_list.append(card)
        return card

    @classmethod
    def get_cards_by_number(cls, number: int) -> set["Card"]:
        cards = list(filter(lambda x: x.number == number, card_list))
        # cards = [card for card in card_list if card.number == number]
        return cards

    def __init__(self, line: str):
        line = " ".join(line.split())
        card, card_data = line.split(":")
        self.number = int(card.replace("Card ", ""))

        card_data = card_data.strip().split(" | ")
        self.line = line
        self.desired_numbers = set(map(int, card_data[0].split()))
        self.actual_numbers = set(map(int, card_data[1].split()))
        self.winning_numbers = self.desired_numbers.intersection(self.actual_numbers)

    def __repr__(self):
        return f"<Card {self.number}>"

    def get_won_cards(self) -> list["Card"]:
        num_winners = len(self.winning_numbers)
        total_new_cards = []
        for i in range(1, num_winners + 1):
            new_cards = Card.get_cards_by_number(self.number + i)
            for n in new_cards:
                total_new_cards.append(n)
                total_new_cards.extend(n.get_won_cards())

        if not total_new_cards:
            return []

        # print(f"Card {self.number} won {len(total_new_cards)} cards")
        # print(f"\tAdding {total_new_cards}")

        return total_new_cards


curr_dir = Path(__file__).parent


def populate_card_dict(test: bool = TEST):
    input_file = curr_dir / "test_input.txt" if test else curr_dir / "input.txt"
    data = input_file.read_text().splitlines()

    for line in data:
        Card.create(line)

    return data


populate_card_dict()

card_list = sorted(card_list, key=lambda x: x.number)
total_cards = copy(card_list)

for c in copy(card_list):
    cards = c.get_won_cards()
    total_cards.extend(cards)


counter = Counter([c.number for c in total_cards])


for k, v in counter.items():
    print(f"Card {k} has {v} cards")


print(len(total_cards))
