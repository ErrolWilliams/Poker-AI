import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
import roomai
import roomai.common
import roomai.texas

random.seed(3)
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

class AI3(roomai.common.AbstractPlayer):
    def recieve_info():
        #code
    def take_action():
        #code
    def reset():
        # code

class AI4(roomai.common.AbstractPlayer):
    def recieve_info():
        #code
    def take_action():
        #code
    def reset():
        # code
"""

def show_public(public_state):
    print ("dealer_id:%d\n"%(public_state.dealer_id) +\
           "chips:%s\n"%(",".join([str(i) for i in public_state.chips])) +\
           "bets:%s\n"%(",".join([str(i) for i in public_state.bets])) +\
           "is_folds:%s\n"%(",".join([str(i) for i in public_state.is_fold])) +\
           "public_cards:%s\n"%(",".join([c.key for c in public_state.public_cards]))
           )

def show_info(info):
    person_state = info.person_state
    print ("%d available_actions: %s"%(person_state.id, ",".join(sorted(person_state.available_actions.keys()))))
    print ("%d cards:%s"%(person_state.id,",".join([c.key for c in person_state.hand_cards])))

#---------------------------------------------------------------

def initial_population():
    initial_games = 1 # number of rounds to play
    training_data = []
    scores = []
    accepted_scores = [] # We want to take the top 25% of winning scores and the top 25% of losing scores

    # Initialize environment

    players     = [roomai.common.RandomPlayerChance(), roomai.common.RandomPlayerChance(),  roomai.common.RandomPlayerChance(), roomai.common.RandomPlayerChance()]
    env         = roomai.texas.TexasHoldemEnv()
    num_players = len(players)

    for _ in range(initial_games):
        score = 0
        game_memory = []
        prev_observations = []

        # Reset Environment

        infos, public_state, person_states, private_state = env.init({"num_normal_players": 4})
        show_public(public_state)
        for i in range(num_players):
            players[i].receive_info(infos[i])
            show_info(infos[i])
        print ("\n")

        #Play till showdown or till all-but-one player folds

        while public_state.is_terminal == False:
            turn = public_state.turn
            action = players[turn].take_action()
            infos, public_state, person_states, private_state = env.forward(action)

            if len(prev_observations) > 0:
                game_memory.append([prev_observation, action])
            
            prev_observations = public_state
            print("Public State")
            show_public(public_state)
            for i in range(num_players):
                print ("INFO")
                players[i].receive_info(infos[i])
                show_info(infos[i])
            print ("\n")

        print (public_state.scores)

        print ("\n\n NEW ROUND \n\n")

initial_population()
#---------------------------------------------------------------
""""
if __name__ == "__main__":
    players     = [roomai.common.RandomPlayerChance(), roomai.common.RandomPlayerChance(),  roomai.common.RandomPlayerChance(), roomai.common.RandomPlayerChance()]
    env         = roomai.texas.TexasHoldemEnv()

    num_players = len(players)

    for _ in range(3):
        infos, public_state, person_states, private_state = env.init({"num_normal_players": 4})
        show_public(public_state)
        for i in range(num_players):
            players[i].receive_info(infos[i])
            show_info(infos[i])
        print ("\n")

        while public_state.is_terminal == False:
            turn = public_state.turn
            action = players[turn].take_action()
            print ("%d player take an action (%s)"%(turn,action.key))
            infos, public_state, person_states, private_state = env.forward(action)
            show_public(public_state)
            for i in range(num_players):
                players[i].receive_info(infos[i])
                show_info(infos[i])
            print ("\n")

        print (public_state.scores)

        print ("\n\n NEW ROUND \n\n")
"""    