import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
from copy import deepcopy
import roomai
import roomai.common
import roomai.texas
from poker.roomai_bot import RoomAIBot

random.seed(14325)
"""
class AI1(roomai.common.AbstractPlayer):
    def recieve_info():
        #code
    def take_action():
        #code
    def reset():
        # code

class AI2(roomai.common.AbstractPlayer):
    def recieve_info():
        #code
    def take_action():
        #code
    def reset():
        # code

"""
#--------------------------------------------------------------

def show_public(public_state):
    print ("dealer_id:%d\n"%(public_state.dealer_id) +\
           "chips:%s\n"%(", ".join([str(i) for i in public_state.chips])) +\
           "bets:%s\n"%(", ".join([str(i) for i in public_state.bets])) +\
           "is_folds:%s\n"%(", ".join([str(i) for i in public_state.is_fold])) +\
           "public_cards:%s\n"%(", ".join([c.key for c in public_state.public_cards]))
           )

def save_public(text, public_state):
    text.write("dealer_id:%d\n"%(public_state.dealer_id) +\
           "chips:%s\r\n"%(" | ".join([str(i) for i in public_state.chips])) +\
           "bets:%s\r\n"%(" | ".join([str(i) for i in public_state.bets])) +\
           "is_folds:%s\r\n"%(" | ".join([str(i) for i in public_state.is_fold])) +\
           "public_cards:%s\r\n"%(" | ".join([c.key for c in public_state.public_cards]))
           )

def show_info(info):
    person_state = info.person_state
    print ("%d available_actions: %s"%(person_state.id, ",".join(sorted(person_state.available_actions.keys()))))
    print ("%d cards:%s"%(person_state.id,",".join([c.key for c in person_state.hand_cards])))

def save_info(text, info):
    person_state = info.person_state
    text.write("Player %d Available Actions: %s"%(person_state.id, "|".join(sorted(person_state.available_actions.keys()))))
    text.write("\r\n")
    text.write("Player %d Cards: %s"%(person_state.id," |  ".join([c.key for c in person_state.hand_cards])))

#----------------------------------------------------------------

def new_game():
    players     = [roomai.common.RandomPlayerChance(), \
                   roomai.common.RandomPlayerChance(), \
                   roomai.common.RandomPlayerChance(), \
                   roomai.common.RandomPlayerChance()]
    env         = roomai.texas.TexasHoldemEnv()
    np = len(players)
    dealer = 0
    chips = [2000 for i in range(np)]
    big_blind = 20
    infos, public_state, person_state, private_state = env.init({"num_normal_players": np, \
                                                                  "dealer_id": dealer,      \
                                                                  "chips": chips,           \
                                                                  "big_blind_bet": big_blind})
    return players, env, np, infos, public_state, person_state, private_state, big_blind
    
#----------------------------------------------------------------
    
def clear_losers(players, ps, big_blind):

    dealer = ps.dealer_id
    new_chips = []
    for i in range(len(ps.chips)-1,-1,-1):
        if ps.chips[i] >= big_blind:
            new_chips.insert(0, ps.chips[i])
        elif i <= dealer:
            del players[i]
            dealer -= 1
        else:
            del players[i]
    
    return players, len(players), dealer, new_chips
    
def next_round(env, players, ps, big_blind):
    print(ps.chips)
    play_list, np, dealer, new_chips = clear_losers(players, ps, big_blind)
    print(new_chips)
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

def play(file, rounds):
    text = open(file, "w")                  # Text file to log game
    num_rounds = rounds                     # number of rounds to play
    text.write("Rounds: ")
    text.write(str(rounds))
    text.write("\r\n\r\n")
    
    # Initialize environment
    players, env, num_players, infos, public_state, person_state, private_state, big_blind = new_game()
    terminal = False
    
    for round_num in range(num_rounds):
        if (round_num % 10) == 9:
            big_blind = big_blind * 2   # Double blind every 10 rounds

        save_public(text, public_state)
        for i in range(num_players):        # Send each player Public_state and Personal info
                players[i].receive_info(infos[i])
                save_info(text, infos[i])
                text.write("\r\n")
                
        # Play till winner
        while public_state.is_terminal == False:
            turn = public_state.turn
            action = players[turn].take_action()
            text.write("Player %d: (%s)"%(turn,action.key))
            text.write("\r\n")
            infos, public_state, person_states, private_state = env.forward(action)

            save_public(text, public_state)
            for i in range(num_players):
                players[i].receive_info(infos[i])
                save_info(text, infos[i])
                text.write("\r\n")
            text.write ("\r\n")

        text.write(str(public_state.scores))

        text.write ("\r\n\r\n NEW ROUND \r\n\r\n")

        player, num_players, infos, public_state, person_state, private_state, terminal = next_round(env, players, public_state, big_blind)

        if terminal:
            print (round_num)   # End Game if Only 1 Player Remains
            break

#----------------------------------------------------------------
if __name__ == "__main__":
    num_epoch = 1       # Number of Epoch (An Epoch is a single cycle of simulation and learning from the simulations.)
    num_rounds = 3      # Number of Rounds per epoch
    for _ in range(num_epoch):
        play("Data.txt", num_rounds)

def train():
	print("Training...")

