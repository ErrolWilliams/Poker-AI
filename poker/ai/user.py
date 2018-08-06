from . import AI

class UserBot(AI):
	def __init__(self):
		super().__init__()
		self.version = 1
	
	def request(self):
		monte_odds = self.get_odds()
		print(f"Odds are: {monte_odds}")
		for index, ac in enumerate(action.enum):
			print(f"{ac.action_name} => {index}")
		num = int(input("Choose an action: "))
		ac = action.enum[num]
		print(f"Using action {ac.action_name}")
		return ac

