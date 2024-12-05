from collections import Counter
from copy import deepcopy
from enum import Enum, auto
from functools import total_ordering
from pathlib import Path

TEST = False
curr_dir = Path(__file__).parent


@total_ordering
class TypeEnum(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()

    def __lt__(self, other: "TypeEnum"):
        return self.value < other.value


class Card:
    ORDER: list[str] = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
    value: str

    def __hash__(self):
        return self.ORDER.index(self.value)

    def __eq__(self, other: "Card"):
        other_val = other.value if isinstance(other, Card) else other
        return self.ORDER.index(self.value) == self.ORDER.index(other_val)

    def __lt__(self, other: "Card"):
        return self.ORDER.index(self.value) < self.ORDER.index(other.value)

    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class Hand:
    original_cards: list["Card"]
    cards: list["Card"]

    bid: int
    rank: int
    hand_parts: list[str]
    hand_type: TypeEnum

    def __repr__(self):
        return f"{self.hand_type.name} {self.cards} {self.bid}"

    def __init__(self, line: str):
        hand, bid = line.split(" ")
        self.cards = [Card(card) for card in hand]
        self.bid = int(bid)
        self.original_cards = deepcopy(self.cards)

    def __lt__(self, other: "Hand"):
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type

        for i in range(len(self.cards)):
            if self.original_cards[i] != other.original_cards[i]:
                return self.original_cards[i] < other.original_cards[i]
        return None

    @staticmethod
    def get_hand_type(cards: list[Card]):
        card_counts = Counter([c.value for c in cards])

        if len(card_counts) == 1:
            return TypeEnum.FIVE_OF_A_KIND
        if len(card_counts) == 2:
            if 3 in card_counts.values():
                return TypeEnum.FULL_HOUSE
            return TypeEnum.FOUR_OF_A_KIND
        if len(card_counts) == 3:
            if 3 in card_counts.values():
                return TypeEnum.THREE_OF_A_KIND
            return TypeEnum.TWO_PAIR
        if len(card_counts) == 4:
            return TypeEnum.ONE_PAIR
        return TypeEnum.HIGH_CARD


def get_data(test: bool = TEST):
    input_file = get_input_file(test)
    data = input_file.read_text()
    return data


def get_input_file(test: bool = TEST):
    input_file = curr_dir / "test_input" if test else curr_dir / "input"
    return input_file


def improve_hand(hand: Hand):
    non_wildcards = [c for c in hand.cards if c != "J"]
    wildcards = [c for c in hand.cards if c == "J"]
    if len(non_wildcards) == 5:
        return hand

    if len(wildcards) == 5:
        hand.cards = [Card("A") for _ in range(5)]
        hand.hand_type = Hand.get_hand_type(hand.cards)
        return hand
    if len(wildcards) == 4:
        for i, c in enumerate(hand.cards):
            if c != "J":
                continue
            hand.cards[i] = Card(non_wildcards[0].value)
        hand.hand_type = Hand.get_hand_type(hand.cards)
        return hand
    if len(wildcards) == 3:
        max_val = max(non_wildcards).value
        for i, c in enumerate(hand.cards):
            if c != "J":
                continue
            hand.cards[i] = Card(max_val)
        hand.hand_type = Hand.get_hand_type(hand.cards)
        return hand

    better_cards = try_better_hand(hand.cards)
    hand.cards = better_cards
    hand.hand_type = Hand.get_hand_type(hand.cards)
    return hand


def try_better_hand(cards: list[Card]):
    best_hand_type = Hand.get_hand_type(cards)
    for i, card in enumerate(cards):
        if card != "J":
            continue
        for card_val in Card.ORDER[1:]:
            new_card = Card(card_val)
            temp_cards = deepcopy(cards)
            temp_cards[i] = new_card
            if Hand.get_hand_type(temp_cards) >= best_hand_type:
                cards = temp_cards
                if Hand.get_hand_type(temp_cards) > best_hand_type:
                    best_hand_type = Hand.get_hand_type(temp_cards)
            elif "J" in temp_cards:
                temp_cards = try_better_hand(temp_cards)

    return cards


data = get_data()

hands: list[Hand] = []
for line in data.splitlines():
    h = Hand(line)
    h.hand_type = Hand.get_hand_type(h.cards)
    hands.append(h)


for i, h in enumerate(hands):
    original_hand_type = h.hand_type
    original_cards = deepcopy(h.cards)
    improved = improve_hand(h)
    assert len(improved.cards) == 5
    if "J" in original_cards and len(set(original_cards)) > 1:
        assert improved.hand_type > original_hand_type

    assert "J" not in h.cards
    hands[i] = improved

    if original_hand_type != improved.hand_type:
        original_cards_str = "".join([str(c) for c in original_cards])
        improved_cards = "".join([str(c) for c in improved.cards])
        print(
            f"{original_hand_type.name:<20} {improved.hand_type.name:<20} {original_cards_str:<15} -> {improved_cards:<20}"
        )


sorted_hands: list[Hand] = sorted(hands)

for i, hand in enumerate(sorted_hands):
    hand.rank = i + 1
    # print(f"{hand.bid:<10} {hand.rank:<10} {hand.bid * (i + 1):<10}")


print(sum([hand.bid * (i + 1) for i, hand in enumerate(sorted_hands)]))
