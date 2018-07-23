from poker.table import Table
from poker.player import Player
import poker.ai.action
from treys import Card

class AI():

	def __init__(self, player_id):
		print("placeholder")
		self.table = Table()
		self.player_id = player_id
		self.player = self.table.get_player(self.player_id)

	def players_active(self):
		num_active = 0
		for player in self.table.players:
			if not player.folded:
				num_active += 1

		return num_active
	
	def card_obj(self, card_str):
		return Card.new(card_str[0] + card_str[1].lower())

	def request_action(self):
		cards = []
		for card_str in self.table.board:
			cards.append(self.card_obj(card_str))

		return action.Call()

	def request_bet(self):
		return action.Call()

	def get_player(self, player_id):
		return self.table.get_player(player_id)



