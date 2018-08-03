import poker
from poker.table import Table
from poker.player import Player
from poker.odds import odds
from poker.ai import action
from treys import Card
from poker.monte import monteCarlo
import poker.tables as tables
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
import sys


class AI():

	def __init__(self):
		self.table = Table()

	def attach(self, player_id):
		self.player_id = player_id
		self.player = self.table.get_player(self.player_id)

	def roomai_update(self, info, public_state):
		self.table.roomai_update(info, public_state)

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

	def get_odds_2(self):
		sys.stdout = open(os.devnull, 'w')
		board = [self.treys_str(x) for x in self.table.board]
		hand = [self.treys_str(x) for x in self.player.cards]

		if len(board) == 0:
			monte_odds = tables.get_chance(self.players_active(), self.player.cards[0], self.player.cards[1])
		else:
			monte_odds = odds(hand, board, self.players_active())

		sys.stdout = sys.__stdout__

		print(f"Used get_odds_2, result {monte_odds}")

		return monte_odds

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
			monte_odds = tables.get_chance(self.players_active(), self.player.cards[0], self.player.cards[1])
		else:
			monte_odds = monteCarlo(board, hand, self.players_active()-1, 2000.0)

		return monte_odds

	def request_bet(self):
		the_action = self.request()
		if the_action.action_name == "check":
			print("CHANAGING CHECK TO FOLD!!!!!!!!!!!! THIS IS SO IMPORTANT")
			return action.Fold()
		return the_action

	def get_player(self, player_id):
		return self.table.get_player(player_id)

class OldBot(AI):

	def __init__(self, model_name="basicPlayer1", version=0):
		super().__init__()
		self.version = version
		poker.model.load(model_name)

	def create_input_1(self):
		print("Generating V1 inputs")
		monte_odds = self.get_odds()
		my_stake = self.player.bet / (self.player.chips + self.player.bet)
		my_chips = self.player.chips / self.table.total_chips()
		my_cost = (max([self.table.players[p].bet for p in self.table.players]) - self.player.bet)/(self.player.chips + self.player.bet)
		state = self.table.round
		pot_percent = self.table.pot()/self.table.total_chips()
		num_players = self.players_active()


		r = np.array([[monte_odds, my_stake, my_chips, my_cost, state, pot_percent, num_players]])
		print(r)
		return r

	def create_input(self):
		if self.version == 1:
			return self.create_input_1()
		print("Generating V0 inputs")

		monte_odds = self.get_odds()
		round_num = self.table.round
		risk = (1-monte_odds) * self.table.num_raise 
		return np.array([[round_num, risk]])

	def request(self):

		model_action = poker.model.get_action(self.create_input())
		monte_odds = self.get_odds()
		print(f"monte_odds={monte_odds} round={self.table.round}")

		if model_action == 'bet':
			return action.Bet(int(self.player.chips*0.15))
		elif model_action == 'call':
			return action.Call()
		elif model_action == 'check':
			return action.Check()
		elif model_action == 'fold':
			if monte_odds > 0.3:
				return action.Call()
			return action.Fold()
		else:
			return action.Raise()
	

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


class StatBot(AI):
	def __init__(self):
		super().__init__()
		self.version = 0

	def request(self):
		monte_odds = self.get_odds()
		round_num = self.table.round

		print("Using stats!")
		print(f"monte_odds={monte_odds} round={self.table.round}")
		if monte_odds > 0.85:
			return action.Bet(int(self.player.chips*0.5))
		elif monte_odds > 0.75:
			return action.Bet(int(self.player.chips*0.2))
		elif monte_odds > 0.60:
			return action.Call()
		elif monte_odds > 0.50 or (monte_odds > 0.15 and round_num == 0):
			return action.Check()
		else:
			return action.Fold()


class StatBot2(AI):
	def __init__(self):
		super().__init__()
		self.version = 0

	def request(self):
		"""
		Constants
		"""
		
		high_risk = 0.2
		med_risk = 0.1
		high_odds = 2.5
		med_odds = 0.9
	
		"""
		"""
		odds = self.get_odds()
		odds = odds / (1/float(self.players_active())) 
		round_num = self.table.round
		chips = self.player.chips
		cur_bet = self.player.min_bet - self.table.small_blind
		my_bet = self.player.bet + self.player.round_bet + self.player.min_bet
		round_risk = my_bet / float(my_bet + chips)
		print('Bet: {0}'.format(self.bet)) 
		print('roundBet: {0}'.format(self.round_bet)) 
		print('minBet: {0}'.format(self.min_bet)) 
		
		print("Using stats!")
		if round_risk > high_risk:
			Risk = 'high'
		elif round_risk > med_risk:
			Risk = 'med'
		else:
			Risk = 'low'
		if odds > high_odds:
			Odds = 'high'
		elif odds > med_odds:
			Odds = 'med'
		else:
			Odds = 'low'
		print('Risk: {0}({1})\nOdds: {2}({3}\nBet: {4})'.format(round_risk, Risk, odds, Odds, cur_bet))
		
		if round_risk > high_risk:     # high risk
			if odds > high_odds:
				if cur_bet > 0:
					return action.Raise()
				else:
					return action.Bet(int(self.player.chips*0.05))
			elif odds > med_odds:
				if cur_bet > 0:
					return action.Call()
				else:
					return action.Check()
			else:
				if cur_bet > 0:
					return action.Fold()
				else:
					return action.Check()
		elif round_risk > med_risk:    # med risk	
			if odds > high_odds:
				if cur_bet > 0:
					return action.Raise()
				else:
					return action.Bet(int(self.player.chips*0.05))
			elif odds > med_odds:
				if cur_bet > 0:
					return action.Call()
				else:
					return action.Check()
			else:
				if cur_bet > 0:
					return action.Fold()
				else:
					return action.Check()
		else:
			if odds > high_odds:
				if cur_bet > 0:
					return action.Raise()
				else:
					return action.Bet(int(self.player.chips*0.1))
			elif odds > med_odds:
				if cur_bet > 0:
					return action.Call()
				else:
					return action.Bet(int(self.player.chips*0.05))
			else:
				if cur_bet > 0:
					return action.Fold()
				else:
					return action.Check()


class QBot(AI):
	def __init__(self):
		super().__init__()
		self.eps = 0.5
		self.decay_factor = 0.999
		self.last_action = None
		self.version = 1

	def create_model(self):
		self.model = keras.Sequential()
		self.model.add(keras.layers.InputLayer(batch_input_shape=(1,7)))
		
		self.model.add(keras.layers.Dense(128, input_shape=(7,), activation='sigmoid'))
		self.model.add(keras.layers.Dense(256, input_shape=(128,), activation='sigmoid'))
		self.model.add(keras.layers.Dense(256, input_shape=(256,), activation='sigmoid'))
		self.model.add(keras.layers.Dense(256, input_shape=(256,), activation='sigmoid'))
		self.model.add(keras.layers.Dense(256, input_shape=(256,), activation='sigmoid'))
		self.model.add(keras.layers.Dense(len(action.enum), input_shape=(256,), activation='linear'))
		self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])

	def load_model(self, model_name):
		model_path = os.path.join(os.path.dirname(sys.argv[0]), "models", model_name)
		self.model = tf.keras.models.load_model(model_path)
		self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])

	def save_model(self, model_name):
		model_path = os.path.join(os.path.dirname(sys.argv[0]), "models", model_name)
		tf.keras.models.save_model(
			self.model,
			model_path,
			overwrite=True,
			include_optimizer=False
        )

	def round_end(self):
		self.reinforce(0)

	def reinforce(self, qmax):
		if self.last_action == None:
			return
		print("Reinforcing!")

		y = 0.95

		last_reward = self.player.chips - self.last_chips
		last_reward_mod = last_reward + y * qmax

		print("Action {} resulted in reward of {}... That's {}!. Reinforcing from {} to {}".format(self.last_action.action_name, last_reward, 'good' if last_reward > 0 else ('bad' if last_reward < 0 else 'very interesting'), self.last_prediction[0][self.last_action.index()], last_reward_mod))

		self.last_prediction[0][self.last_action.index()] = last_reward_mod
		self.model.fit(self.last_input, self.last_prediction, epochs=1, verbose=0)


		self.last_action = None

	def create_input_q(self):
		monte_odds = self.get_odds()
		round_num = self.table.round
		raised = self.table.num_raise
		total_chips = float(self.table.total_chips())
		chips_percent = self.player.chips/total_chips
		pot_percent = self.table.pot()/total_chips
		num_players = self.players_active()
		return np.array([[monte_odds, round_num, raised, chips_percent, pot_percent, total_chips, num_players]])

	def request(self):
		the_input = self.create_input_q()
		prediction = self.model.predict(the_input)

		self.reinforce(np.max(prediction))

		self.eps *= self.decay_factor
		print(f"EPS: {self.eps}")
		if np.random.random() < self.eps:
			print("Taking random action")
			next_action = action.Action.random()
		else:
			print("Taking predicted action")
			next_action = action.Action.from_index(np.argmax(prediction))

		self.last_input = the_input
		self.last_prediction = prediction
		self.last_action = next_action
		self.last_chips = self.player.chips
		return next_action



