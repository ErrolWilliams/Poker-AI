
class Player(object):
	def __init__(self, playername):
		self.playername = playername
		self.folded = False

	def roomai_update(self, info, public_state):
		self.chips = public_state.chips[self.playername]
		self.round_bet = public_state.bets[self.playername]
		if info.person_state.id == self.playername:
			self.cards = [x.key[0] + x.key[2] for x in info.person_state.hand_cards]

		pass

	def json_update(self, json_obj):
		self.chips = json_obj["chips"]
		self.folded = json_obj["folded"]
		self.allIn = json_obj["allIn"]
		self.isSurvive = json_obj["isSurvive"]
		self.reloadCount = json_obj["reloadCount"]
		self.round_bet = json_obj["roundBet"]
		self.bet = json_obj["bet"]
		if 'cards' in json_obj:
			self.cards = json_obj['cards']
		
