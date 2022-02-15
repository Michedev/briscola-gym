from briscola_gym.game_rules import select_winner
from briscola_gym.card import Card, Seed


def test_winner_1_same_seed():
    card1 = Card(3, 1)
    card2 = Card(9, 1)
    briscola = Card(1, 3)
    assert int(select_winner([card1, card2], briscola)) == 0


def test_winner_2_same_seed():
    card1 = Card(2, 1)
    card2 = Card(1, 1)
    briscola = Card(1, 3)
    assert select_winner([card1, card2], briscola) == 1


def test_winner_1_different_seed():
    card1 = Card(4, 1)
    card2 = Card(1, 2)
    briscola = Card(1, 3)
    assert select_winner([card1, card2], briscola) == 0


def test_winner_2_different_seed_briscola():
    card1 = Card(1, 1)
    card2 = Card(2, 3)
    briscola = Card(1, 3)
    assert select_winner([card1, card2], briscola) == 1

def test_winner_1_briscola():
    card1 = Card(4, 1)
    card2 = Card(1, 3)
    briscola = Card(1, 1)
    assert select_winner([card1, card2], briscola) == 0