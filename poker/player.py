
class Player(object):
	def __init__(self, playername):
		self.playername = playername
		self.folded = False
		self.min_bet = 0
		self.my_id = 0

	def roomai_update(self, info, public_state):
		self.chips = public_state.chips[self.playername]
		self.bet = public_state.bets[self.playername]
		if info.person_state.id == self.playername:
			self.cards = [x.key[0] + x.key[2] for x in info.person_state.hand_cards]
			print(self.cards)

		pass
		self.folded = public_state.is_fold  # player's fold status
		self.allIn = False                  # TODO
		self.isSurvive = True               # TODO 
		self.reloadCount = 0                # no reloads in roomai
		self.round_bet = public_state.bets[self.my_id]

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
		if 'minBet' in json_obj:
			self.min_bet = json_obj['minBet']
			
