import json

class Action(object):

	def __init__(self):
		self.action_name = "action goes here"

	def to_json(self):
		return {
			"eventName" : "__action",
			"data" : {
				"action" : self.action_name
			}
		}
	
	def to_roomai(self):
		return ""

class Bet(Action):

	def __init__(self, amount):
		self.amount = amount
		self.action_name = "bet"

	def to_json():
		obj = super(Action, self).to_json()
		obj["data"]["amount"] = self.amount
		return obj

class Call(Action):
	def __init__(self):
		self.action_name = "call"

class Check(Action):
	def __init__(self):
		self.action_name = "check"

class Fold(Action):
	def __init__(self):
		self.action_name = "fold"

class Raise(Action):
	def __init__(self):
		self.action_name = "raise"

class AllIn(Action):
	def __init__(self):
		self.action_name = "allin"


