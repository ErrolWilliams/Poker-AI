from . import AI
from . import action
import poker
import numpy as np

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
	

