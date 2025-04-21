from typing import List
import random
from texasholdem import TexasHoldEm, ActionType

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

class Agent: 
    def play(self, game):
        pass
    def __init__(self):
        pass
#TODO: Write an agent that does random actions (game has a method that returns available actions)

class Game:
    def __init__(self, agents, max_players):
        #TODO: Pass arguments to this
        self.game = TexasHoldEm(500, 10, 5, max_players = max_players)
        self.agents = agents
        
    def play_hand(self):
        self.game.start_hand()
        #TODO: Write fundamental game loop, passing game to agents and letting them play
        
    


