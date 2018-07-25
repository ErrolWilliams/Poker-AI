from poker.table import Table
from poker.player import Player
from poker.odds import odds
from poker.model import get_action
import poker.ai.action
from treys import Card
from poker.monte import monteCarlo
import poker.tables as tables
import numpy as np

STATS = False

class AI():

	def __init__(self, player_id):
		print("placeholder")
		self.table = Table()
		self.player_id = player_id
		self.player = self.table.get_player(self.player_id)
		self.eps = 0.5
		self.decay_factor = 0.999
		self.action_enum = [action.Bet(), action.Call(), action.Check(), action.Fold(), action.Raise(), action.AllIn()]

	def roomai_update(self, info, public_state):
		self.table.roomai_update(info, public_state)


	def random_action(self):
		return random.choice([action.Bet(), action.Call(), action.Check(), action.Fold(), action.Raise(), action.AllIn()])


	def players_active(self):
		num_active = 0
		for playername in self.table.players:
			player = self.table.players[playername]
			if not player.folded:
				num_active += 1

		return num_active
	
	def card_obj(self, card_str):
		return Card.new(card_str[0].upper() + card_str[1].lower())

	def create_input(self):
		return []

	def reinforce(self, qmax):
		if self.last_action == None:
			return

		y = 0.95

		last_reward = calculate_the_last_reward_based_on_the_data_we_got_since_the_last_request() #todo
		last_reward = last_reward + y * qmax
		self.last_prediction[self.last_action.index()] = last_reward
		self.model.fit(self.last_input, self.last_prediction, epochs=1, verbose=0)

	def reinforce(self):
		self.reinforce(0)

	def request(self):
		the_input = self.create_input()
		prediction = self.model.predict(the_input)

		self.reinforce(np.max(prediction))

		self.eps *= self.decay_factor
		if np.random.random() < self.eps:
			next_action = action.Action.random()
		else:
			next_action = action.Action.from_index(np.argmax(prediction))

		self.last_input = the_input
		self.last_prediction = prediction
		self.last_action = next_action
		return next_action

	def request_action(self):
		board = []
		hand = []

		for card_str in self.table.board:
			board.append(self.card_obj(card_str))

		for card_str in self.player.cards:
			hand.append(self.card_obj(card_str))

		print(f"HAND2: {self.player.cards} HAND3: {hand}")

		round_num = self.table.round


		if len(board) == 0:
			monte_odds = tables.get_chance(self.players_active(), self.player.cards[0], self.player.cards[1])
		else:
			monte_odds = monteCarlo(board, hand, self.players_active()-1, 2000.0)
	
		if STATS:
			print("Using stats!")
			if monte_odds > 0.95:
				return action.Bet(int(self.player.chips*0.5))
			elif monte_odds > 0.75:
				return action.Bet(int(self.player.chips*0.2))
			elif monte_odds > 0.50:
				return action.Check()
			elif monte_odds > 0.25:
				return action.Call()
			else:
				return action.Fold()

		risk = (1-monte_odds) * self.table.num_raise 
		model_action = get_action(round_num, risk)

		if model_action == 'bet':
			return action.Bet(int(self.player.chips*0.15))
		elif model_action == 'call':
			return action.Call()
		elif model_action == 'check':
			return action.Check()
		elif model_action == 'fold':
			return action.Fold()
		else:
			return action.Raise()
	
	def request_bet(self):
		return self.request_action()

	def get_player(self, player_id):
		return self.table.get_player(player_id)



