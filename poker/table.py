from poker.player import Player
class Table(object):
	def __init__(self):
		self.chips = 0
		self.folded = False
		self.players = dict()
		self.board = []
		self.num_raise = 0

	def get_player(self, player_id):
		if not(player_id in self.players):
			self.players[player_id] = Player(player_id)

		return self.players[player_id]
	
	def print_state(self):
		print(f"Chips: {self.chips}")
		
	
	
	def json_update(self, json_data_obj):
		print('updating table')
		self.json = json_data_obj
		self.round_name = self.json['roundName']
		self.board = self.json['board']
		self.raise_count = self.json['raiseCount']
		self.bet_count = self.json['betCount']

		round_names = ["Deal", "Flop", "Turn", "River"]
		self.round = round_names.index(self.round_name)
