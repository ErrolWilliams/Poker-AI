from . import AI
import numpy as np
from tensorflow import keras
from . import action
import os
import sys

class QBot(AI):
	def __init__(self, load=None, save=None, eps=0.5, plot=True):
		super().__init__()
		self.eps = eps
		self.decay_factor = 0.999
		self.last_action = None
		self.version = 0
		np.set_printoptions(suppress=True)
		self.load_model(load)
		self.game_num = 0
		self.num_wins = 0
		self.save_model_name = save
		self.plot_enabled = False

		if plot:
			self.plot_init()

	def create_model(self):
		self.model = keras.Sequential()
		self.model.add(keras.layers.InputLayer(batch_input_shape=(1,4)))	
		self.model.add(keras.layers.Dense(128, input_shape=(4,), activation='sigmoid'))
		self.model.add(keras.layers.Dense(256, input_shape=(128,), activation='sigmoid'))
		self.model.add(keras.layers.Dense(256, input_shape=(256,), activation='sigmoid'))
		self.model.add(keras.layers.Dense(256, input_shape=(256,), activation='sigmoid'))
		self.model.add(keras.layers.Dense(256, input_shape=(256,), activation='sigmoid'))
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
		self.reinforce(0)

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
			self.update_plot(self.game_num, self.num_wins / PERIOD)
			self.num_wins = 0
		self.num_wins += self.did_i_win()
		self.game_num += 1

	def cleanup(self):
		self.save_model()

	def reinforce(self, qmax):
		if self.last_action == None:
			return
		# print("Reinforcing!")

		y = 0.95

		last_reward = self.player.chips - self.last_chips
		last_reward_mod = last_reward + y * qmax
		# print(f'Last input was {self.last_input}')
		# print("Action {} resulted in reward of {}... That's {}!. Reinforcing from {} to {}".format(self.last_action.action_name, last_reward, 'good' if last_reward > 0 else ('bad' if last_reward < 0 else 'very interesting'), self.last_prediction[0][self.last_action.index()], last_reward_mod))

		self.last_prediction[0][self.last_action.index()] = last_reward_mod
		self.model.fit(self.last_input, self.last_prediction, epochs=1, verbose=0)


		self.last_action = None

	def create_input_q(self):
		monte_odds = self.get_odds()
		round_num = self.table.round
		raised = self.table.num_raise
		total_chips = float(self.table.total_chips())
		chips_percent = self.player.chips/total_chips
		risk = self.player.bet/(self.player.bet + self.player.chips)
		pot_percent = self.table.pot()/total_chips
		num_players = self.players_active()
		return np.array([[round(monte_odds,1), round(round_num,1), round(risk,1), round(num_players,1)]])

	def request(self):
		the_input = self.create_input_q()
		prediction = self.model.predict(the_input)
		# print(prediction)

		self.reinforce(np.max(prediction))

		# self.eps *= self.decay_factor   moved to game_end
		# print(f"EPS: {self.eps}")
		if np.random.random() < self.eps:
			# print("Taking random action")
			next_action = action.Action.random()
		else:
			# print("Taking predicted action")
			next_action = action.Action.from_index(np.argmax(prediction))

		self.last_input = the_input
		self.last_prediction = prediction
		self.last_action = next_action
		self.last_chips = self.player.chips
		return next_action


