from typing import List, Sequence
import numpy as np
import random
from abc import ABC, abstractmethod
from texasholdem import TexasHoldEm, ActionType, History

# Action types
FOLD = 0
CHECK = 1
CALL = 2
RAISE = 3

# Betting states

PREFLOP = 0
FLOP = 1
TURN = 2
RIVER = 3
SHOWDOWN = 4

generator = np.random.default_rng()

def truncated_exponential(scale = 0.1):
    amount = generator.exponential(scale=3)
    while amount > 1:
        amount = generator.exponential(scale=3)
    return amount

class Agent(ABC): 
    @abstractmethod
    def play(self, game: TexasHoldEm) -> tuple[ActionType, int | None]:
        pass
#TODO: Write an agent that does random actions (game has a method that returns available actions)
class RandomAgent(Agent):
    def play(self, game: TexasHoldEm):
        moves = game.get_available_moves()
        actions = moves.action_types
        action = random.sample(actions, 1)[0]
        if action == ActionType.RAISE:
            min_amt, max_amt = min(moves.raise_range), max(moves.raise_range)
            
            amount = generator.exponential(scale=3)
            while amount > 1:
                amount = generator.exponential(scale=3)
            print(amount)
            amount = int(amount * (max_amt - min_amt) + min_amt)
            return action, amount
        else:
            return action, None
    def __init__(self):
        pass

class Game:
    def __init__(self, agents: Sequence[Agent], max_players):
        #TODO: Pass arguments to this
        self.game = TexasHoldEm(500, 10, 5, max_players = max_players)
        self.agents = agents
        self.hand_histories : List[History] = []
        
    def play_hand(self) -> bool:
        #https://texasholdem.readthedocs.io/en/0.11/
        self.game.start_hand()
        if self.game.is_hand_running():
            #TODO: Write fundamental game loop, passing game to agents and letting them play
            while self.game.is_hand_running():
                action, amount = self.agents[self.game.current_player].play(self.game)
                self.game.take_action(action, total = amount)
            if self.game.hand_history is not None:
                self.hand_histories.append(self.game.hand_history)
            return True
        else:
            print("Failed starting hand")
            print(f"Game is {self.game.game_state}")
            print(f"Player chips are {[self.game.players[i].chips for i in range(len(self.game.players))]}")
            return False
            
if __name__ == "__main__":
    
    agents = [RandomAgent() for _ in range(6)]
    game = Game(agents, 6)
    for i in range(50):
        print(f"Playing Hand {i}")
        if not game.play_hand():
            print("Game over")
            break
        print("HAND HISTORY:")
        print(game.hand_histories[-1].to_string())
    print(f"Player chips are {[game.game.players[i].chips for i in range(len(game.game.players))]}")
    


