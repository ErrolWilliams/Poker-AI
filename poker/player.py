
class Player(object):
	def __init__(self, md5):
		self.playername = md5

	def __init__(self):
		pass
	def json_update(self, json_obj):
		self.chips = json_obj["chips"]
		self.folded = json_obj["folded"]
		self.allIn = json_obj["allIn"]
		self.isSurvive = json_obj["isSurvive"]
		self.reloadCount = json_obj["reloadCount"]
		self.roundBet = json_obj["roundBet"]
		self.bet = json_obj["bet"]
		
