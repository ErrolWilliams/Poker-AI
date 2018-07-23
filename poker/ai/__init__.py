from poker.table import Table
from poker.player import Player
from poker.odds import odds
from poker.model import action
import poker.ai.action
from treys import Card

class AI():

	def __init__(self, player_id):
		print("placeholder")
		self.table = Table()
		self.player_id = player_id
		self.player = self.table.get_player(self.player_id)
	
	def card_obj(self, card_str):
		return Card.new(card_str[0] + card_str[1].lower())

	def request_action(self):
		board = []
                hand = []
		for card_str in self.table.board:
			board.append(self.card_obj(card_str))
                for card_str in player.cards:
                        hand.append(self.card_obj(card_str))
                round_num = self.table.round
                monte_odds = odds(hand, board, self.players_active())
                risk = (1-monte_odds) * self.table.num_raise 
                model_action = action(round_num, risk)
                if model_action == 'bet':
                        return acton.Bet()
                elif model_action == 'call':
                        return action.Call()
                elif model_action == 'check':
                        return action.Check():
                elif model_action == 'fold':
                        return action.Fold()
                else:
                        return action.Raise()
	
        def request_bet(self):
		return action.Call()

	def get_player(self, player_id):
		return self.table.get_player(player_id)



