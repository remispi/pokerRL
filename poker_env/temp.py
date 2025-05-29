from typing import List
import numpy as np
import random
from abc import ABC, abstractmethod
from texasholdem import TexasHoldEm, ActionType, agents

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
    def play(self, game: TexasHoldEm):
        moves = game.get_available_moves()
        actions = moves.action_types
        action = random.sample(actions, 1)[0]
        if action == ActionType.RAISE:
            min_amt, max_amt = min(moves.raise_range), max(moves.raise_range)
            
            amount = generator.exponential(scale=3)
            while amount > 1:
                amount = generator.exponential(scale=3)
            amount = amount * (max_amt - min_amt) + min_amt
            return action, amount
        else:
            return action, None
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
            amount = amount * (max_amt - min_amt) + min_amt
            return action, amount
        else:
            return action, None
    def __init__(self):
        pass

class Game:
    def __init__(self, agents: List[Agent], max_players):
        #TODO: Pass arguments to this
        self.game = TexasHoldEm(500, 10, 5, max_players = max_players)
        self.agents = agents
        self.hand_histories = []
        
    def play_hand(self):
        #https://texasholdem.readthedocs.io/en/0.11/
        self.game.start_hand()
        if self.game.is_hand_running():
            #TODO: Write fundamental game loop, passing game to agents and letting them play
            while self.game.is_hand_running():
                action, amount = self.agents[self.game.current_player].play(self.game)
                self.game.take_action(action, total=amount)
            self.hand_histories.append(self.game.hand_history)
        else:
            print("Game is over, can't play hand")
            
if __name__ == "__main__":
    game = TexasHoldEm(500, 10, 5, max_players=4)
    agent = RandomAgent()
    game.start_hand()
    print(agent.play(game))
    if not game.is_hand_running():
        print("Game over")
    while game.is_hand_running():
            print(agent.play(game))
            action, amount = agents.random_agent(game)
            # print(f"Player {game.current_player} {action} {amount}")
            game.take_action(action, total=amount)
    print(game.hand_history.to_string())
    data = np.array([truncated_exponential(scale=3) for _ in range(20)])
    print(np.mean(data, axis=0), np.std(data, axis=0), data)
    


