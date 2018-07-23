from poker.table import Table
from poker.player import Player
from poker.odds import odds
from poker.model import get_action
import poker.ai.action
from treys import Card
from poker.monte import monteCarlo

class AI():

	def __init__(self, player_id):
		print("placeholder")
		self.table = Table()
		self.player_id = player_id
		self.player = self.table.get_player(self.player_id)

	def players_active(self):
		num_active = 0
		for playername in self.table.players:
			player = self.table.players[playername]
			if not player.folded:
				num_active += 1

		return num_active
	
	def card_obj(self, card_str):
		return Card.new(card_str[0] + card_str[1].lower())

	def request_action(self):
		board = []
		hand = []

		for card_str in self.table.board:
			board.append(self.card_obj(card_str))

		for card_str in self.player.cards:
			hand.append(self.card_obj(card_str))

		print(f"HAND2: {self.player.cards} HAND3: {hand}")

		round_num = self.table.round

		if len(board) == 0:
			monte_odds = 0.75
		else:
			monte_odds = monteCarlo(board, hand, self.players_active()-1, 2000.0)

		risk = (1-monte_odds) * self.table.num_raise 
		model_action = get_action(round_num, risk)

		if model_action == 'bet':
			return action.Bet(int(self.player.chips*0.15))
		elif model_action == 'call':
			return action.Call()
		elif model_action == 'check':
			return action.Check()
		elif model_action == 'fold':
			return action.Fold()
		else:
			return action.Raise()
	
	def request_bet(self):
		return self.request_action()

	def get_player(self, player_id):
		return self.table.get_player(player_id)



