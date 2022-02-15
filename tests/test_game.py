from briscola_gym.game import BriscolaRandomPlayer


def test_game():
    game = BriscolaRandomPlayer()
    game.reset()
    done = False
    assert True