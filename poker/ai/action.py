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

	
	def to_roomai(self, ai, available_actions):
		exit()
		return ""

	def get_roomai_action_random(self, available_actions):
		print(f"Falling back to random action instead of {self}! You may want to fix this!")
		print(available_actions.keys())
		exit()
		return random.choice(list(available_actions.items()))[1]

	def get_roomai_action_prefix(self, available_actions, *names):
		keys = available_actions.keys()
		for name in names:
			for key in keys:
				if key.startswith(name):
					return available_actions[key]

		return self.get_roomai_action_random(available_actions)
	
	def get_roomai_action_num(self, available_actions, number):
		action_nums = [int(x.split('_')[1]) for x in available_actions.keys()]
		num_idx = 0	
		while action_nums[num_idx] < number and (num_idx < len(action_nums)-1):
			num_idx += 1
		if num_idx > 0:
			if abs(action_nums[num_idx-1] - number) < abs(action_nums[num_idx] - number):
				num_idx -= 1
		action = [available_actions[key] for key in available_actions if str(action_nums[num_idx]) in key]
		return action[0]

	def get_roomai_action(self, available_actions, *names):
			
		for name in names:
			if name in available_actions:
				return available_actions[name]
		return self.get_roomai_action_random(available_actions)
	

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

	def to_roomai(self, ai, available_actions):
		return self.get_roomai_action_num(available_actions, self.amount)

class Call(Action):
	def __init__(self):
		self.action_name = "call"

	def index(self):
		return 1

	def to_roomai(self, ai, available_actions):
		#call_amount = ai.table.
		return self.get_roomai_action_prefix(available_actions, 'Call', 'Fold_0')

class Check(Action):
	def __init__(self):
		self.action_name = "check"

	def index(self):
		return 2

	def to_roomai(self, ai, available_actions):
		return self.get_roomai_action_prefix(available_actions, 'Check_0', 'Fold_0')

class Fold(Action):
	def __init__(self):
		self.action_name = "fold"

	def index(self):
		return 3

	def to_roomai(self, ai, available_actions):
		return self.get_roomai_action(available_actions, 'Fold_0')

class Raise(Action):
	def __init__(self):
		self.action_name = "raise"

	def index(self):
		return 4

	def to_roomai(self, ai, available_actions):
		raise_amount = ai.table.small_blind*2 + ai.player.max_bet_sofar
		return self.get_roomai_action_num(available_actions, raise_amount)

class AllIn(Action):
	def __init__(self):
		self.action_name = "allin"

	def index(self):
		return 5

	def to_roomai(self, ai, available_actions):
		return self.get_roomai_action_prefix(available_actions, 'Allin_')

enum = [Bet(), Call(), Check(), Fold(), Raise(), AllIn()]

