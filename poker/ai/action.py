import json
import random


class Action(object):

	@staticmethod
	def from_index(index):
		return enum[index]

	@staticmethod
	def random():
		return random.choice(enum)

	def __init__(self):
		self.action_name = "action goes here"

	def to_json(self):
		print(f"CONVERTING {self.action_name} TO JSON")
		return {
			"eventName" : "__action",
			"data" : {
				"action" : self.action_name
			}
		}

	
	def to_roomai(self):
		return ""

	def index(self):
		return -1

class Bet(Action):

	def __init__(self, amount=0):
		self.amount = amount
		self.action_name = "bet"

	def to_json(self):
		obj = super().to_json()
		obj["data"]["amount"] = self.amount
		print(f"BET AMOUNT: {self.amount}")
		return obj

	def index(self):
		return 0

class Call(Action):
	def __init__(self):
		self.action_name = "call"

	def index(self):
		return 1


class Check(Action):
	def __init__(self):
		self.action_name = "check"

	def index(self):
		return 2


class Fold(Action):
	def __init__(self):
		self.action_name = "fold"

	def index(self):
		return 3


class Raise(Action):
	def __init__(self):
		self.action_name = "raise"

	def index(self):
		return 4


class AllIn(Action):
	def __init__(self):
		self.action_name = "allin"

	def index(self):
		return 5


enum = [Bet(), Call(), Check(), Fold(), Raise(), AllIn()]

