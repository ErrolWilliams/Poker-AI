from poker.player import Player
class Table(object):
	def __init__(self):
		
		self.chips = 0
		self.folded = False
		self.players = dict()
		self.board = []
		self.bet_count = 0
		self.raise_count = 0
		self.round = -1

	@property
	def num_raise(self):
		return self.bet_count + self.raise_count

	def total_chips(self):
		return sum([self.players[p].chips + self.players[p].bet for p in self.players])

	def pot(self):
		return sum([self.players[p].bet for p in self.players])


	def get_player(self, player_id):
		if not(player_id in self.players):
			self.players[player_id] = Player(player_id)

		return self.players[player_id]
	
	def print_state(self):
		print(f"Chips: {self.chips}")
		
	def roomai_update(self, info, public_state):
		for i in range(len(public_state.chips)):
			self.get_player(i).roomai_update(info, public_state)

		self.board = [x.key for x in public_state.public_cards]
		self.round = [0, 3, 4, 5].index(len(self.board))
	
	def json_update(self, json_data_obj):
		self.json = json_data_obj
		self.round_name = self.json['roundName']
		self.board = self.json['board']
		self.raise_count = self.json['raiseCount']
		self.bet_count = self.json['betCount']
                self.big_blind = self.json['bigBlind']['amount']
                round_names = ["Deal", "Flop", "Turn", "River", "Showdown"]
		self.round = round_names.index(self.round_name)
