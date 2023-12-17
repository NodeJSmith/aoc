from collections import Counter
from enum import Enum, auto
from pathlib import Path

TEST = False
curr_dir = Path(__file__).parent


class TypeEnum(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


class Card:
    ORDER: list[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    value: str

    def __lt__(self, other: "Card"):
        return self.ORDER.index(self.value) < self.ORDER.index(other.value)

    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


class Hand:
    cards: list["Card"]
    card_counts: dict[str, int]
    bid: int
    rank: int

    def __repr__(self):
        return f"{self.hand_type.name} {self.cards} {self.bid}"

    def __init__(self, line: str):
        hand, bid = line.split(" ")
        self.cards = [Card(card) for card in hand]
        self.card_counts = Counter([c.value for c in self.cards])
        self.bid = int(bid)

    def __lt__(self, other: "Hand"):
        if self.hand_type != other.hand_type:
            return self.hand_type.value < other.hand_type.value

        for i in range(len(self.cards)):
            if self.cards[i].value != other.cards[i].value:
                return self.cards[i] < other.cards[i]

    @property
    def hand_type(self):
        if len(self.card_counts) == 1:
            return TypeEnum.FIVE_OF_A_KIND
        if len(self.card_counts) == 2:
            if 3 in self.card_counts.values():
                return TypeEnum.FULL_HOUSE
            return TypeEnum.FOUR_OF_A_KIND
        if len(self.card_counts) == 3:
            if 3 in self.card_counts.values():
                return TypeEnum.THREE_OF_A_KIND
            return TypeEnum.TWO_PAIR
        if len(self.card_counts) == 4:
            return TypeEnum.ONE_PAIR
        return TypeEnum.HIGH_CARD


def get_data(test: bool = TEST):
    input_file = get_input_file(test)
    data = input_file.read_text()
    return data


def get_input_file(test: bool = TEST):
    input_file = curr_dir / "test_input" if test else curr_dir / "input"
    return input_file


data = get_data()

hands: list[Hand] = []
for line in data.splitlines():
    hands.append(Hand(line))

sorted_hands: list[Hand] = sorted(hands)

for i, hand in enumerate(sorted_hands):
    hand.rank = i + 1
    print(f"{hand.bid:<10} {hand.rank:<10} {hand.bid * (i + 1):<10}")


print(sum([hand.bid * (i + 1) for i, hand in enumerate(sorted_hands)]))
