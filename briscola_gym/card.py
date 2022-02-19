from dataclasses import dataclass, field
from briscola_gym.game_rules import values_points
from briscola_gym.seed import Seed
from random import shuffle


@dataclass()
class Card:
    value: int
    seed: int

    def __post_init__(self):
        assert 0 <= self.value <= 10, self.value
        assert 0 <= self.seed <= 4, self.seed
        self.points = values_points[self.value]

    def vector(self) -> tuple:
        return self.value, self.seed


class Deck:
    __slots__ = ['cards']

    def __init__(self):
        self.cards = self.all_cards()
        shuffle(self.cards)

    @classmethod
    def all_cards(cls):
        return [Card(i % 10 + 1, Seed.get_seed(i // 10)) for i in range(40)]

    def draw(self):
        return self.cards.pop(0)

    def is_empty(self) -> bool:
        return len(self.cards) == 0
