from typing import List, Sequence
import numpy as np
import random
from abc import ABC, abstractmethod
from texasholdem import TexasHoldEm, ActionType, History
from pettingzoo import AECEnv
import gymnasium
from gymnasium.utils import seeding
from pettingzoo.utils import AgentSelector

class raw_env(AECEnv):
    metadata = {"render_modes": ["human"], "name" : "nlhe_v0"}
    def __init__(self, render_mode = None):
        self.possible_agents = [f"player_{i}" for i in range(6)]
        self.agent_name_mapping = dict(enumerate(self.possible_agents))
        self.render_mode = render_mode
        
    def reset(self, seed=None, options=None):
        self.np_random, self.np_random_seed = seeding.np_random(seed)
        self.agents = self.possible_agents[:]
        self.rewards = {agent : 0 for agent in self.agents}
        self._cumulative_rewards = {agent : 0 for agent in self.agents}
        self.terminations = {agent : False for agent in self.agents}
        self.trunctations = {agent : False for agent in self.agents}
        self.infos = {agent : {} for agent in self.agents}
        self.num_moves = 0
        self._agent_selector = AgentSelector(self.agents)
        self.agent_selection = self._agent_selector.next()
        if options is None: 
            options = {}
        self.game = TexasHoldEm( \
            buyin=options.get("buyin", 500),
            big_blind=options.get("big_blind", 10),
            small_blind=options.get("small_blind", 5),
            max_players=6,
        )
        
    

generator = np.random.default_rng()

def truncated_exponential(scale = 0.1):
    amount = generator.exponential(scale)
    while amount > 1:
        amount = generator.exponential(scale)
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
            return False
            
if __name__ == "__main__":
    
    agents = [RandomAgent() for _ in range(6)]
    game = Game(agents, 6)
    for i in range(30):
        print(f"Playing Hand {i}")
        if not game.play_hand():
            print("Game over")
            break
        print("HAND HISTORY:")
        print(game.hand_histories[-1].to_string())
    print(f"Player chips are {[game.game.players[i].chips for i in range(len(game.game.players))]}")
    


