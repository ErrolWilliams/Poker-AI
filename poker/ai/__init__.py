import poker
#import poker.lookup
from poker.table import Table
from poker.player import Player
from poker.odds import odds
from poker.monte import monteCarlo
from poker.ai import action
from treys import Card


class AI():

	def __init__(self):
		self.table = Table()

	@property
	def name(self):
		return self.__class__.__name__

	def attach(self, player_id):
		self.player_id = player_id
		self.player = self.table.get_player(self.player_id)

	def players_active(self):
		num_active = 0
		for playername in self.table.players:
			player = self.table.players[playername]
			if not player.folded:
				num_active += 1

		return num_active

	def treys_str(self, card_str):
		return card_str[0].upper() + card_str[1].lower()
	
	def card_obj(self, card_str):
		return Card.new(card_str[0].upper() + card_str[1].lower())

	def round_end(self):
		pass

	def get_odds(self):
		if self.version == 1:
			return self.get_odds_2()
		board = []
		hand = []
		

		for card_str in self.table.board:
			board.append(self.card_obj(card_str))

		for card_str in self.player.cards:
			hand.append(self.card_obj(card_str))

		if len(board) == 0:
			monte_odds = lookup.get_chance(self.players_active(), self.player.cards[0], self.player.cards[1])
		else:
			monte_odds = monteCarlo(board, hand, self.players_active()-1, 2000.0)

		return monte_odds

	def get_odds_2(self):
		sys.stdout = open(os.devnull, 'w')
		board = [self.treys_str(x) for x in self.table.board]
		hand = [self.treys_str(x) for x in self.player.cards]

		if len(board) == 0:
			monte_odds = lookup.get_chance(self.players_active(), self.player.cards[0], self.player.cards[1])
		else:
			monte_odds = odds(hand, board, self.players_active())

		sys.stdout = sys.__stdout__

		print(f"Used get_odds_2, result {monte_odds}")

		return monte_odds


	def request_bet(self):
		the_action = self.request()
		return the_action

	def get_player(self, player_id):
		return self.table.get_player(player_id)





