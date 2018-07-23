from poker.table import Table
from poker.player import Player
import poker.ai.action

class AI():

	def __init__(self, player_id):
		print("placeholder")
		self.table = Table()
		self.player_id = player_id
		self.player = self.table.get_player(self.player_id)

	def request_action(self):
		return action.Call()

	def request_bet(self):
		return action.Call()

	def get_player(self, player_id):
		return self.table.get_player(player_id)



