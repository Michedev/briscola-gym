from briscola_gym.card import Card
from briscola_gym.game import BriscolaRandomPlayer


def test_state_update_after_winner():
    game = BriscolaRandomPlayer()
    game.reset()
    game.turn_my_player = 0
    game.table = [Card(1, 1), Card(1,3)]
    reward = game._state_update_after_winner(i_winner=0)
    assert reward == 22
    assert game.turn_my_player == 0
    assert game.points == [22, 0]

def test_state_update_after_lose():
    game = BriscolaRandomPlayer()
    game.reset()
    game.turn_my_player = 0
    game.table = [Card(1, 1), Card(1,3)]
    reward = game._state_update_after_winner(i_winner=1)
    assert reward == -22
    assert game.points == [22, 0]
    assert game.turn_my_player == 1