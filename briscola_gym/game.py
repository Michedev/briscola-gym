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
            'my_points': spaces.Discrete(120),
            'other_points': spaces.Discrete(120),
            'hand_size': spaces.Discrete(3),
            'hand': spaces.Tuple([card_space, card_space, card_space]),
            'table': spaces.Tuple([card_space, card_space]),
            'my_discarded': spaces.Tuple([card_space] * 40),
            'other_discarded': spaces.Tuple([card_space] * 40),
            'turn': spaces.Discrete(40),
            'briscola': card_space,
            'order': spaces.Discrete(1)
        })
        self.deck = None
        self.briscola: Card = None
        self.__logger = logging.getLogger('Briscola')
        self.turn_my_player = 0

    def step(self, action):
        assert action in self.action_space
        self.turn += 1
        my_card = self.my_player.hand.pop(action)
        self.table.append(my_card)
        if self.turn_my_player == 0:
            other_card = self.other_player.discard_card()
            self.table.append(other_card)
        self.__logger.info(f'Table: {self.table}')
        i_winner = select_winner(self.table, self.briscola)
        reward = self._state_update_after_winner(i_winner)
        self._draw_phase()
        if self.turn_my_player == 1:
            other_card = self.other_player.discard_card()
            self.table.append(other_card)
        return self.public_state().as_dict(), reward, self.is_finish(), dict()

    def _state_update_after_winner(self, i_winner):
        self.__logger.info(f'Turn Winner is {self.players[i_winner].name}')
        reward = gained_points = sum(values_points[c.value] for c in self.table)
        self.points[0] += gained_points
        self.my_discarded.append(self.table[self.turn_my_player])
        self.other_discarded.append(self.table[1 - self.turn_my_player])
        gained_points_my_player = gained_points_other_player = gained_points
        if i_winner == self.turn_my_player:
            self.my_points += gained_points
            self.turn_my_player = 0
            gained_points_other_player = gained_points_other_player * -1
        else:
            self.other_points += gained_points
            self.turn_my_player = 1
            gained_points_my_player = gained_points_my_player * -1
            reward = reward * -1
        self.my_player.notify_turn_winner(gained_points_my_player)
        self.other_player.notify_turn_winner(gained_points_other_player)
        self.table = []
        self.__logger.info(f'Winner gained {gained_points} points')
        self.__logger.info(f'Current table points: {self.points}')
        return reward

    def _draw_phase(self):
        if not self.deck.is_empty():
            c1 = self.deck.draw()
            if self.deck.is_empty():
                c2 = self.briscola
            else:
                c2 = self.deck.draw()
            if self.turn_my_player == 0:
                c_my_player = c1
                c_other_player = c2
            else:
                c_other_player = c1
                c_my_player = c2
            self.my_player.hand.append(c_my_player)
            self.other_player.hand.append(c_other_player)

    def public_state(self):
        return PublicState(self.my_points, self.other_points, self.my_player.hand,
                           self.table, self.my_discarded, self.other_discarded,
                           self.turn, self.briscola, self.turn_my_player)


    def is_finish(self):
        return any(p > 60 for p in self.points) or \
               (self.deck.is_empty() and all(len(p.hand) == 0 for p in self.players))

    def reset(self):
        self.turn = 0
        self.my_player: BasePlayer = HumanPlayer()
        self.other_player: BasePlayer = PseudoRandomPlayer()
        self.deck = Deck()
        self.my_discarded = []
        self.table = []
        self.other_discarded = []
        self.my_points = 0
        self.other_points = 0
        self.points = [0, 0]
        self.turn_my_player = randint(0, 1)
        self.players = [self.my_player, self.other_player]
        self.briscola: Card = self.deck.draw()
        for _ in range(3):
            self.my_player.hand.append(self.deck.draw())
        for _ in range(3):
            self.other_player.hand.append(self.deck.draw())
        if self.turn_my_player == 1:
            other_card = self.other_player.discard_card()
            self.table.append(other_card)


    def render(self, mode="human"):
        pass
