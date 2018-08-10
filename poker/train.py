import pdb
import roomai
from roomai import common, texas
import poker.ai
import random
import time
from poker.ai import AI
from poker.ai.old import OldBot
from poker.ai.stat import StatBot, StatBot2
from poker.ai.qbot import QBot
from poker.ai.user import UserBot

score_rounds = []
ai_scores = []


class BlackPanther(object):
    
	def __init__(self, ai):
		self.ai = ai
		
	def receive_info(self, info):
		self.update_ai(info, info.public_state)
		self.available_actions = info.person_state.available_actions

	def update_ai(self, info, public_state):
		self.ai.attach(info.person_state.id)
		self.ai.table.roomai_update(info, public_state)

	def take_action(self):
		action = self.ai.request()
		return action.to_roomai(self.ai, self.available_actions)
		
	def round_end(self, info):
		self.update_ai(info, info.public_state)
		self.ai.round_end()

#--------------------------------------------------------------
def random_ai():
	def make_qbot():
		r = QBot(load='nachos')
		return r
	
	ais = [
		# make_qbot,
		lambda: StatBot(),
		lambda: StatBot2()
	]
	return random.choice(ais)()

def new_game(ai, num_players):
    players = []
    players.append(BlackPanther(ai))
    for i in range(num_players):
        players.append(BlackPanther(random_ai()))
    env         = roomai.texas.TexasHoldemEnv()
    np          = len(players)
    dealer      = 0
    chips       = [2000 for i in range(np)]
    big_blind   = 20
    
    infos, public_state, person_state, private_state = env.init({"num_normal_players": np, \
                                                                  "dealer_id": dealer,      \
                                                                  "chips": chips,           \
                                                                  "big_blind_bet": big_blind})
    return players, env, np, infos, public_state, person_state, private_state, big_blind
    
def clear_losers(players, ps, big_blind):

    dealer      = ps.dealer_id
    new_chips   = []
    
    for i in range(len(ps.chips)-1,-1,-1):
        if ps.chips[i] > big_blind:
            new_chips.insert(0, ps.chips[i])
        elif i <= dealer:
            del players[i]
            dealer -= 1
        else:
            del players[i]
    
    return players, len(players), dealer, new_chips
    
def next_round(env, players, ps, big_blind):
    
    play_list, np, dealer, new_chips = clear_losers(players, ps, big_blind)
    dealer = (dealer + 1)%np
    if len(new_chips) <= 1:
        terminal = True
    else:
        terminal = False
    infos, public_state, person_state, private_state = env.init({"num_normal_players": np, \
                                                                  "dealer_id": dealer,      \
                                                                  "chips": new_chips,           \
                                                                  "big_blind_bet": big_blind})
    return play_list, np, infos, public_state, person_state, private_state, terminal

#------------------------------------------------------------------

def play(rounds, ai, num_players):
    players, env, num_players, infos, public_state, person_state, private_state, big_blind = new_game(ai, num_players)
    terminal = False
    
    for round_num in range(rounds):

        if (round_num % 10) == 9:
            big_blind = big_blind * 2   # Double blind every 10 rounds
            
        for i in range(num_players):    # Send each player Public_state and Personal info
                players[i].receive_info(infos[i])
                
        # Play till winner
        while public_state.is_terminal == False:
            turn = public_state.turn
            action = players[turn].take_action()
            infos, public_state, person_states, private_state = env.forward(action)

            for i in range(num_players):
                players[i].receive_info(infos[i])

        player, num_players, infos, public_state, person_state, private_state, terminal = next_round(env, players, public_state, big_blind)

        for i in range(num_players):
            players[i].round_end(infos[i])

        if terminal:
            break

#----------------------------------------------------------------

def compete_stats(ai, num_players):
	players, env, num_players, infos, public_state, person_state, private_state, big_blind = new_game(ai, num_players)
	scores = env.compete(env,players)
	return scores[ai.player_id]	

#----------------------------------------------------------------
plot_init = False
def update_plot():
	global plot_init
	try:
		import matplotlib.pyplot as plt
		if not plot_init:
			plt.ion()
			plt.show()
			plot_init = True
		plt.plot(score_rounds, ai_scores)
		plt.draw()
		plt.pause(0.001)
	except Exception as e:
		print(f'Couldn\'t plot the plot: {e}')
#----------------------------------------------------------------

def train(ai):
	global score_rounds
	global ai_scores
	num_epoch   = 10000   # Number of Epoch (An Epoch is a single cycle of simulation and learning from the simulations.)
	num_rounds  = 50     # Number of Rounds per epoch

	for i in range(num_epoch):
		print('Game {0}'.format(i+1))
		num_play    = random.choice([4,5,6,7,8,9])
		play(num_rounds, ai, num_play)
		ai.game_end()
		if i % 100 == 0:      # every 100 games compete and save win percent
			score_rounds.append(float(i))
			ai_scores.append(compete_stats(ai, num_play))
			update_plot()
	update_plot()	
