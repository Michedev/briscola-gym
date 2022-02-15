from briscola_gym.card import Deck, Card

def test_all_cards():
    expected = [Card(value=1, seed=1), Card(value=1, seed=2), Card(value=1, seed=3), Card(value=1, seed=4),
                Card(value=2, seed=1), Card(value=2, seed=2), Card(value=2, seed=3), Card(value=2, seed=4),
                Card(value=3, seed=1), Card(value=3, seed=2), Card(value=3, seed=3), Card(value=3, seed=4),
                Card(value=4, seed=1), Card(value=4, seed=2), Card(value=4, seed=3), Card(value=4, seed=4),
                Card(value=5, seed=1), Card(value=5, seed=2), Card(value=5, seed=3), Card(value=5, seed=4),
                Card(value=6, seed=1), Card(value=6, seed=2), Card(value=6, seed=3), Card(value=6, seed=4),
                Card(value=7, seed=1), Card(value=7, seed=2), Card(value=7, seed=3), Card(value=7, seed=4),
                Card(value=8, seed=1), Card(value=8, seed=2), Card(value=8, seed=3), Card(value=8, seed=4),
                Card(value=9, seed=1), Card(value=9, seed=2), Card(value=9, seed=3), Card(value=9, seed=4),
                Card(value=10, seed=1), Card(value=10, seed=2), Card(value=10, seed=3), Card(value=10, seed=4)]
    expected = sorted(expected, key=lambda c: c.value + c.seed * 10)

    actual = Deck.all_cards()
    actual = sorted(actual, key=lambda c: c.value + c.seed * 10)

    for i in range(len(expected)):
        assert expected[i] == actual[i]
