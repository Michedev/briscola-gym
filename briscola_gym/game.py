import logging
from random import randint

from briscola_gym.player.base_player import BasePlayer
from gym import spaces

from briscola_gym.state import PublicState

from briscola_gym.game_rules import select_winner
from briscola_gym.card import *
import gym

from briscola_gym.player.random_player import PseudoRandomPlayer
from briscola_gym.player.human_player import HumanPlayer


class BriscolaRandomPlayer(gym.Env):

    def __init__(self):
        self.action_space = spaces.Discrete(3)  # drop i-th card
        self.reward_range = (-22, 22)
        card_space = spaces.Tuple((spaces.Discrete(11), spaces.Discrete(5)))  # (value, seed)
        self.observation_space = spaces.Dict({
            'points': spaces.MultiDiscrete([120, 120]),
            'hand_size': spaces.Discrete(3),
            'hand': spaces.Tuple([card_space, card_space, card_space]),
            'table': spaces.Tuple([card_space, card_space]),
            'discarded': spaces.Tuple([card_space] * 40),
            'turn': spaces.Discrete(40),
            'briscola': card_space,
            'order': spaces.Discrete(1)
        })
        self.deck = None
        self.briscola = None
        self.__logger = logging.getLogger('Briscola')
        self.turn_my_player = 0

    def step(self, action):
        assert action in self.action_space
        self.turn += 1
        my_card = self._my_player.hand.pop(action)
        self.table.append(my_card)
        if self.turn_my_player == 0:
            other_card = self._other_player.discard_card()
            self.table.append(other_card)
        self.__logger.info(f'Table: {self.table}')
        i_winner = select_winner(self.table, self.briscola)
        self.__logger.info(f'Turn Winner is {self.players[i_winner].name}')
        self.players[0], self.players[1] = self.players[i_winner], self.players[1 - i_winner]
        self.points[0], self.points[1] = self.points[i_winner], self.points[1 - i_winner]
        reward = gained_points = sum(values_points[c.value] for c in self.table)
        self.points[0] += gained_points
        self.discarded += self.table
        if i_winner == self.turn_my_player:
            self.turn_my_player = 0
        else:
            reward = reward * -1
            self.turn_my_player = 1
        self.players[0].notify_turn_winner(gained_points)
        self.players[1].notify_turn_winner(- gained_points)
        self.table = []
        self.__logger.info(f'Winner gained {gained_points} points')
        self.__logger.info(f'Current table points: {self.points}')
        self._draw_phase()
        if self.turn_my_player == 1:
            other_card = self._other_player.discard_card()
            self.table.append(other_card)
        return self.public_state().as_dict(), reward, self.is_finish(), dict()

    def _draw_phase(self):
        if not self.deck.is_empty():
            c1 = self.deck.draw()
            if self.deck.is_empty():
                c2 = self.briscola
            else:
                c2 = self.deck.draw()
            self.players[0].hand.append(c1)
            self.players[1].hand.append(c2)
            self.__logger.info(f'{self.players[0].name} draws {c1}')
            self.__logger.info(f'{self.players[1].name} draws {c2}')

    def public_state(self):
        return PublicState(self.points, self._my_player.hand,
                           self.table, self.discarded,
                           self.turn, self.briscola, self.turn_my_player)


    def is_finish(self):
        return any(p > 60 for p in self.points) or \
               (self.deck.is_empty() and all(len(p.hand) == 0 for p in self.players))

    def reset(self):
        self.turn = 0
        self._my_player: BasePlayer = HumanPlayer()
        self._other_player: BasePlayer = PseudoRandomPlayer()
        self.deck = Deck()
        self.discarded = []
        self.points = [0, 0]
        self.turn_my_player = randint(0, 1)
        self.players = [self._my_player, self._other_player]
        self.briscola = self.deck.draw()
        for _ in range(3):
            self._my_player.hand.append(self.deck.draw())
        for _ in range(3):
            self._other_player.hand.append(self.deck.draw())

    def render(self, mode="human"):
        pass
