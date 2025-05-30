from typing import Sequence
from tinygrad.tensor import Tensor
import texasholdem
import numpy as np

class NeuralAgent():
    def __init__(self, game:texasholdem.TexasHoldEm):
        self.game = game
    def _suit_to_int(self, suit: int) -> int:
        """texasholdem library suits are fucked
        
        1 = spade 2 = heart 4 = diamond 8 = club
        
        this function returns:
        0 = spade 1 = heart 2 = diamond 3 = club
        
        Raises ValueError if not valid input"""
        match suit:
            case 1:
                return 0
            case 2:
                return 1
            case 4:
                return 2
            case 8:
                return 3
            case _:
                raise ValueError("Suit not in {1,2,4,8}")
                

    def hole_embedding(self, cards: tuple[texasholdem.Card, texasholdem.Card]):#
        assert cards[0] != cards[1],  "Hole has the same card twice"
        embedding = np.zeros((4,13), dtype=np.float32)
        embedding[self._suit_to_int(cards[0].suit), cards[0].rank] = 1
        embedding[self._suit_to_int(cards[1].suit), cards[1].rank] = 1
         
    def card_embedding(self, card: texasholdem.Card) -> Tensor:
        rank:int = card.rank
        suit:int = self._suit_to_int(card.suit)
        embedding = np.zeros((4,13), dtype=np.float32)
        embedding[suit, rank] = 1
        return Tensor(embedding)

    def action_embedding(self, action: texasholdem.PlayerAction):
        player_id = action.player_id
        assert(player_id >= 0 and player_id < 6)
        player_id = Tensor(player_id).one_hot(6)
        
        bet = np.zeros(6)
        action_type = Tensor(action.action_type.value).one_hot(5)
        match action.value:
            case None:
                action_value = Tensor(0)
            case _:
                action_value = (Tensor(1 + (action.value / self.game.big_blind))).log()
        bet += action_type.pad((0,1)).numpy()
        bet[5] = action_value.item()
        bet = Tensor(bet)
        print(player_id.numpy()) 
        print(bet.numpy())
        return player_id.cat(bet)
    
    def actions_embedding(self, actions: Sequence[texasholdem.PlayerAction]):
        
        assert(len(actions) <= 6)
        for action in actions:
            player_id = action.player_id
            assert(player_id >= 0 and player_id < 6)
            player_id = Tensor(player_id).one_hot(6)
            
            bet = np.zeros(6)
            action_type = Tensor(action.action_type.value).one_hot(5).numpy()
            match action.value:
                case None:
                    action_value = 0
                case _:
                    action_value = (Tensor(action.value / self.game.big_blind) + 1).log2()
            bet += action_type
            bet[5] = action_value
            bet = Tensor(bet)
            
            pass
        
action = texasholdem.PlayerAction(2, texasholdem.ActionType.RAISE, 150, 100)
game = texasholdem.TexasHoldEm(500, 10, 5, 6)

agent = NeuralAgent(game)
print(agent.action_embedding(action).numpy())