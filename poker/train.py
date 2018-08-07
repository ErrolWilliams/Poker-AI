import roomai
from roomai import common, texas
import poker.ai
import random
from poker.ai import AI
from poker.ai.old import OldBot
from poker.ai.stat import StatBot, StatBot2
from poker.ai.qbot import QBot
from poker.ai.user import UserBot


class BlackPanther(object):
    
	def __init__(self, ai):
		self.ai = ai
		
	def receive_info(self, info, public_state):
		self.update_ai(info, public_state)
		self.available_actions = info.person_state.available_actions
		print(public_state.public_cards)
		print(info.person_state.hand_cards)

	def update_ai(self, info, public_state):
		self.ai.attach(info.person_state.id)
		self.ai.table.roomai_update(info, public_state)

	def take_action(self):
		action = self.ai.request()
		print(self.available_actions)
		return action.to_roomai(self.ai, self.available_actions)
		
	def round_end(self, info, public_state):
		self.update_ai(info, public_state)
		self.ai.round_end()

#--------------------------------------------------------------
def random_ai():
	def make_qbot():
		r = QBot(load='nachos')
		return r
	
	ais = [
		make_qbot,
		lambda: StatBot(),
		lambda: StatBot2()
	]
	return random.choice(ais)()

def new_game(ai, num_players):
    players = []
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
        print(str(round_num))

        if (round_num % 10) == 9:
            big_blind = big_blind * 2   # Double blind every 10 rounds
            
        for i in range(num_players):    # Send each player Public_state and Personal info
                players[i].receive_info(infos[i], public_state)
                
        # Play till winner
        while public_state.is_terminal == False:
            turn = public_state.turn
            print(num_players)
            action = players[turn].take_action()
            infos, public_state, person_states, private_state = env.forward(action)

            for i in range(num_players):
                players[i].receive_info(infos[i], public_state)

        player, num_players, infos, public_state, person_state, private_state, terminal = next_round(env, players, public_state, big_blind)

        for i in range(num_players):
            players[i].round_end(infos[i], public_state)

        if terminal:
            break

#----------------------------------------------------------------
def train(ai):
    num_epoch   = 100     # Number of Epoch (An Epoch is a single cycle of simulation and learning from the simulations.)
    num_rounds  = 50     # Number of Rounds per epoch
    
    num_play    = random.choice([4,5,6,7,8,9,10])
    
    training_data = []
    round_data = []
    for i in range(num_play):
        round_data.append([])
    
    for i in range(num_epoch):
        print(f'Starting Game {i}!')
        for i in range(num_play):
            round_data.append([])
        play(num_rounds, ai, num_play)
        from copy import deepcopy

    print("PUMPKIN: " + str(training_data))
