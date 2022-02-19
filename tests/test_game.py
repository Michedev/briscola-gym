from briscola_gym.card import Card
from briscola_gym.game import BriscolaRandomPlayer


def test_state_update_after_winner():
    game = BriscolaRandomPlayer()
    game.reset()
    game.turn_my_player = 0
    game.table = [Card(1, 1), Card(1, 3)]
    reward = game._state_update_after_winner(i_winner=0)
    assert reward == 22
    assert game.turn_my_player == 0
    assert game.my_points == 22
    assert game.other_points == 0


def test_state_update_after_lose():
    game = BriscolaRandomPlayer()
    game.reset()
    game.turn_my_player = 0
    game.table = [Card(1, 1), Card(1, 3)]
    reward = game._state_update_after_winner(i_winner=1)
    assert reward == -22
    assert game.my_points == 0
    assert game.other_points == 22
    assert game.turn_my_player == 1


def test_single_step_first_my_player():
    game = BriscolaRandomPlayer()
    game.reset()
    game.table = []
    game.turn_my_player = 0
    game.my_player.hand = [Card(1, game.briscola.seed), Card(1, game.briscola.seed), Card(1, game.briscola.seed)]
    game.other_player.hand = [Card(3, game.briscola.seed), Card(3, game.briscola.seed), Card(3, game.briscola.seed)]

    state, reward, done, _ = game.step(0)
    assert not done
    assert reward == 21
    assert game.my_points == 21
    assert game.other_points == 0
    assert state['my_discarded'] == [(1, game.briscola.seed)] + [(0, 0)] * 39
    assert state['other_discarded'] == [(3, game.briscola.seed)] + [(0, 0)] * 39


def test_single_step_first_other():
    game = BriscolaRandomPlayer()
    game.reset()
    game.turn_my_player = 1
    game.my_player.hand = [Card(1, game.briscola.seed), Card(1, game.briscola.seed), Card(1, game.briscola.seed)]
    game.other_player.hand = [Card(3, game.briscola.seed), Card(3, game.briscola.seed)]
    game.table = [Card(3, game.briscola.seed)]
    state, reward, done, _ = game.step(0)
    assert not done
    assert reward == 21
    assert game.my_points == 21
    assert game.other_points == 0
    assert state['my_discarded'] == [(1, game.briscola.seed)] + [(0, 0)] * 39
    assert state['other_discarded'] == [(3, game.briscola.seed)] + [(0, 0)] * 39


def test_100_games():
    import random
    random.seed(100)
    game = BriscolaRandomPlayer()
    for _ in range(100):
        game.reset()
        done = False
        while not done:
            state, reward, done, _ = game.step(0)
            assert (state['my_points'] + state['other_points']) <= 120
            actual_num_cards = len([x for x in state['my_discarded'] if x != (0, 0)]) + \
                               len([x for x in state['other_discarded'] if x != (0, 0)]) + (
                                       len(state['hand']) + len(state['table'])) * 2
            assert actual_num_cards <= 50, actual_num_cards
