import json
import random
from roomai.texas.TexasHoldemAction import AllTexasActions


class Action(object):

	@staticmethod
	def from_index(index):
		return enum[index]

	@staticmethod
	def random():
		return random.choice(enum)

	def __init__(self):
		self.action_name = "action goes here"

	def __str__(self):
		return self.action_name

	def to_json(self):
		print(f"CONVERTING {self.action_name} TO JSON")
		return {
			"eventName" : "__action",
			"data" : {
				"action" : self.action_name
			}
		}

	
	def to_roomai(self, available_actions):
		print("BAD! THIS SHOULDNT BE CALLED!")
		exit()
		return ""

	def get_roomai_action(self, available_actions, *names):

		for name in names:
			if name in available_actions:
				return available_actions[name]
				
		print(f"Falling back to random action instead of {self}! You may want to fix this!")
		exit()
		return random.choice(list(available_actions.items()))[1]

	def index(self):
		return -1

class Bet(Action):

	def __init__(self, amount=0):
		self.amount = amount
		self.action_name = "bet"

	def __str__(self):
		return f"{super().__str__()} (Amount {self.amount})"

	def to_json(self):
		obj = super().to_json()
		obj["data"]["amount"] = self.amount
		print(f"BET AMOUNT: {self.amount}")
		return obj

	def index(self):
		return 0

	def to_roomai(self, available_actions):
		return self.get_roomai_action(available_actions, 'Raise_30', 'Raise_40')

class Call(Action):
	def __init__(self):
		self.action_name = "call"

	def index(self):
		return 1

	def to_roomai(self, available_actions):
		return self.get_roomai_action(available_actions, 'Call_10')

class Check(Action):
	def __init__(self):
		self.action_name = "check"

	def index(self):
		return 2

	def to_roomai(self, available_actions):
		return self.get_roomai_action(available_actions, 'Raise_30', 'Raise_40')

class Fold(Action):
	def __init__(self):
		self.action_name = "fold"

	def index(self):
		return 3

	def to_roomai(self, available_actions):
		return self.get_roomai_action(available_actions, 'Fold_0')

class Raise(Action):
	def __init__(self):
		self.action_name = "raise"

	def index(self):
		return 4

	def to_roomai(self, available_actions):
		return self.get_roomai_action(available_actions, 'Raise_30', 'Raise_40')

class AllIn(Action):
	def __init__(self):
		self.action_name = "allin"

	def index(self):
		return 5

	def to_roomai(self, available_actions):
		return self.get_roomai_action(available_actions, 'Allin_1980', 'Allin_1990')

enum = [Bet(), Call(), Check(), Fold(), Raise(), AllIn()]

