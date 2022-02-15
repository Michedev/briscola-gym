from dataclasses import dataclass
from typing import Tuple, List

from briscola_gym.card import Card


def pad_card_vector(lst: list, max_len: int):
    if len(lst) < max_len:
        for _ in range(max_len - len(lst)):
            lst.append([0, 0])
    return lst


@dataclass(frozen=True)
class PublicState:
    points: Tuple[int, int]
    hand: List[Card]
    table: List[Card]
    discarded: List[Card]
    turn: int
    briscola: Card
    my_turn_player: int

    def as_dict(self) -> dict:
        return dict(
            points=self.points,
            hand_size=len(self.hand),
            hand=pad_card_vector([c.vector() for c in self.hand], 3),
            table=pad_card_vector([c.vector() for c in self.table], 2),
            discarded=pad_card_vector([c.vector() for c in self.discarded], 40),
            turn=self.turn,
            briscola=self.briscola.vector(),
            order=self.my_turn_player
        )

