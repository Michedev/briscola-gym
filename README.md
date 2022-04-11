# Briscola Gym Environment

Implementation of Briscola game Gym Environment. Briscola is a discrete time multi-agent game
where the objective is to take, at the end of the game, more valuable cards than the adversary.

## [Game rules (Wikipedia)](https://en.wikipedia.org/wiki/Briscola#Game_play)


![](https://en.wikipedia.org/wiki/File:Carte_napoletane_al_completo.jpg "Briscola cards")

## Game rules optimization

Theoretically, the match ends when all cards are thrown but a condition shortcut is when one of the player reach more than 60 points. 
This implementation takes advantage of this trick to play more matches in a fixed time-frame.

## Gym Environments

Currently, there are three Gym environments for briscola which pick a different adversary AI:

- ```BriscolaCustomEnemyPlayer``` allows you to pass an instance of your custom adversary, allowing for example self-play
- ```BriscolaRandomPlayer``` The enemy AI just throws cards randomically
- ```BriscolaEpsGreedyPlayer```  The enemy AI with probability _p_ use a random strategy, like the RandomPlayer and 
with probability _(1 - p)_ uses a greedy strategy.

## Define a custom Player AI

In order to  define a new player, make a new class which subclasses ```BasePlayer```

Down below an example with ```EpsGreedyPlayer``` class:
```python
from briscola_gym.player.base_player import BasePlayer
from random import randint, random
from briscola_gym.game_rules import select_winner



class EpsGreedyPlayer(BasePlayer):

    def __init__(self, epsilon):
        super().__init__()
        self.epsilon = epsilon
        self.name = 'EpsGreedyPlayer'

    def choose_card(self) -> int:
        if self.epsilon > random():
            return randint(0, len(self.hand)-1) if len(self.hand) > 1 else 0
        return self.greedy_action()

    def greedy_action(self):
        im_first = self.get_public_state().order[0] == self.name
        if im_first:
            return self.card_min_points()
        else:
            return self.card_max_gain()

    def card_max_gain(self):
        i_max = -1
        max_gain = -100
        state = self.get_public_state()
        table = state.table[:]
        table.append(None)
        for i, c in enumerate(self.hand):
            table[-1] = c
            winner = select_winner(table, state.briscola)
            coef_pts = 1 if winner else -1
            gain = coef_pts * sum(map(lambda c: c.points, table))
            if gain > max_gain:
                i_max = i
                max_gain = gain
        return i_max

    def card_min_points(self):
        i_min = -1
        min_pts = 1000
        for i, c in enumerate(self.hand):
            if c.points < min_pts:
                i_min = i
                min_pts = c.points
        return i_min


```
Note: if your player has an internal state for the current game,
remember to overwrite the method ```reset_player()```


## State

### Card representation

Each card is represented by a triple (value, seed, points) where
- value is the card represented number, in range [1, 10]
- Seed is one of the four seeds, represented by a number in range [1, 4]
- points is the corresponding points carried by the card, in range [0, 11]

The tuple (0,0,0) is the _null_ cards. 
### State elements

- my_points: int  | Player points, in range [0, 120]
- other_points: int | Adversary player points, in range[0, 120]
- hand: List[Card]  | An array of three cards, where each card is represented as described above. In case 
the cards are less than three, there will be _null_ cards.
- other_hand_size: int | Number of cards in the hand of the enemy
- remaining_deck_cards: int | Number of cards remaining in the deck
- table: List[Card] | Cards onto the table.
- my_discarded: List[Card]  | The list of discarded card by Player. It has length 40
- other_discarded: List[Card] | The list of discarded cards by the adversary. It has length 40
- turn: int  | The current turn
- briscola: Card | The briscola card
- my_turn_player: int | Tells if, in this turn, we are the first or second player. In range [0, 1]
