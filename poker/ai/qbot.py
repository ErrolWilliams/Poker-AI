from . import AI
import numpy as np
from tensorflow import keras
from . import action
import os
import sys

class QBot(AI):
	def __init__(self, load=None, save=None, eps=0.5, plot=True, gen=0, reinforce=True):
		super().__init__()
		
		generations = [
			{'create_input': self.create_input_0, 'input_size': 4, 'reward': self.reward_0},
			{'create_input': self.create_input_1, 'input_size': 5, 'reward': self.reward_1}
		]

		self.gen = generations[gen]

		self.eps = eps
		self.decay_factor = 0.999
		self.last_action = None
		self.version = 0
		np.set_printoptions(suppress=True)
		self.load_model(load)
		self.game_num = 0
		self.num_wins = 0
		self.win_history = []
		self.save_model_name = save
		self.plot_enabled = False
		self.reinforce_enabled = reinforce

		if plot:
			self.plot_init()

	def create_model(self):
		input_size = self.gen['input_size']
		self.model = keras.Sequential()
		self.model.add(keras.layers.InputLayer(batch_input_shape=(1,input_size)))	
		self.model.add(keras.layers.Dense(128, input_shape=(input_size,), activation='relu'))
		self.model.add(keras.layers.Dense(256, input_shape=(128,), activation='relu'))
		self.model.add(keras.layers.Dense(256, input_shape=(256,), activation='relu'))
		self.model.add(keras.layers.Dense(256, input_shape=(256,), activation='relu'))
		self.model.add(keras.layers.Dense(256, input_shape=(256,), activation='relu'))
		self.model.add(keras.layers.Dense(len(action.enum), input_shape=(256,), activation='linear'))
		self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])

	def load_model(self, model_name):
		if not model_name:
			self.create_model()
			return

		model_path = os.path.join(os.path.dirname(sys.argv[0]), "qmodels", model_name)
		self.model = keras.models.load_model(model_path)
		self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])

	def save_model(self, num=None):
		if not self.save_model_name:
			return
		name = self.save_model_name if not num else f'{self.save_model_name}-{num}'
		model_path = os.path.join(os.path.dirname(sys.argv[0]), "qmodels", name)
		keras.models.save_model(
			self.model,
			model_path,
			overwrite=True,
			include_optimizer=False
        )
		print(f'Saved model to {name}')

	def round_end(self):
		self.reinforce(0, verbose=True)
		self.last_action = None
		if self.reinforce_enabled:
			pass

	def plot_init(self):
		try:
			import matplotlib.pyplot as plt
			plt.ion()
			plt.show()
			print('plt.show()')
			self.score_rounds = []
			self.ai_scores = []
			self.plot_enabled = True
		except Exception as e:
			print(f'Couldn\'t plot the plot: {e}')
			

	def update_plot(self, x, y):
		print('call to update_plot')
		if not self.plot_enabled:
			return
		try:
			import matplotlib.pyplot as plt
			self.score_rounds.append(x)
			self.ai_scores.append(y)
			plt.plot(self.score_rounds, self.ai_scores)
			plt.draw()
			plt.pause(0.001)
			print('Plotted game_num: {}, score_%: {}'.format(x,y))
		except Exception as e:
			print('plot error: {}'.format(e))
	
	def game_end(self):
		PERIOD = 100

		if self.game_num % 2 == 0:	
			self.eps *= self.decay_factor
		if self.game_num % PERIOD == 0:      #save model every 100 games
			print('Saving model at game {0}'.format(self.game_num))
			self.save_model(self.game_num)

		self.win_history.append(self.did_i_win())
		self.game_num += 1

		if len(self.win_history) > PERIOD:
			self.win_history = self.win_history[-PERIOD:]
			win_percent = sum(self.win_history) / PERIOD
		else:
			win_percent = sum(self.win_history) / len(self.win_history)
		self.update_plot(self.game_num, win_percent)

	def cleanup(self):
		self.save_model()

	def reward_0(self, verbose=False):
		if verbose:
			pass
#print('{} -> {}'.format(self.last_chips, self.player.chips))
		return self.player.chips - self.last_chips


	def reward_1(self, verbose=False):
		last_reward = 0
		if self.chips_percent > 0.25:
			last_reward = self.chips_percent * 10
		elif self.chips_percent > 0.75:
			last_reward = self.chips_percent * 15
		elif self.chips_percent > 0.9:
			last_reward = self.chips_percent * 25
		return last_reward


	def reinforce(self, qmax, verbose=False):
		if (not self.reinforce_enabled) or self.last_action == None:
			return

		y = 0.5
		last_reward = self.gen['reward'](verbose)
		last_reward_mod = last_reward + y * qmax
		# print(f'Last input was {self.last_input}')
		if verbose and (True or self.player.chips == 0):
			print("({} -> {}) Action {} resulted in reward of {}... That's {}!. Reinforcing from {} to {}".format(self.last_chips, self.player.chips, self.last_action.action_name, last_reward, 'good' if last_reward > 0 else ('bad' if last_reward < 0 else 'very interesting'), self.last_prediction[0][self.last_action.index()], last_reward_mod))

		self.last_prediction[0][self.last_action.index()] = last_reward_mod
		self.model.fit(self.last_input, self.last_prediction, epochs=1, verbose=0)


		self.last_action = None

	def create_input(self):
		return self.gen['create_input']()

	def create_input_1(self):
		monte_odds = self.get_odds()
		round_num = self.table.round
		raised = self.table.num_raise
		total_chips = float(self.table.total_chips())
		self.chips_percent = self.player.chips/total_chips
		risk = self.player.bet/(self.player.bet + self.player.chips)
		pot_percent = self.table.pot()/total_chips
		num_players = self.players_active()
		return np.array([[round(monte_odds,1), round(round_num,1), round(risk,1), round(num_players,1), round(self.chips_percent,1)]])

	def create_input_0(self):
		monte_odds = self.get_odds()
		round_num = self.table.round
		raised = self.table.num_raise
		total_chips = float(self.table.total_chips())
		self.chips_percent = self.player.chips/total_chips
		risk = self.player.bet/(self.player.bet + self.player.chips)
		pot_percent = self.table.pot()/total_chips
		num_players = self.players_active()


		return np.array([[round(monte_odds,1), round(round_num,1), round(risk,1), round(num_players,1)]])

	def request(self):
		if self.reinforce_enabled:
			pass
		the_input = self.create_input()
		prediction = self.model.predict(the_input)
		#print(prediction)

		self.reinforce(np.max(prediction), verbose=False)

		# self.eps *= self.decay_factor   moved to game_end
		# print(f"EPS: {self.eps}")
		
		if np.random.random() < self.eps:
			next_action = action.Action.random()
		else:
			next_action = action.Action.from_index(np.argmax(prediction))
			if self.reinforce_enabled:
				pass
#print('predicted {}'.format(next_action))

		self.last_input = the_input
		self.last_prediction = prediction
		self.last_action = next_action
		self.last_chips = self.player.chips
		self.last_chips_percent = self.chips_percent
		return next_action


