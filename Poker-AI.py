#!/usr/bin/python3

import tensorflow as tf
tf.enable_eager_execution()
from poker import client
from poker.model import load
import argparse
import poker.tables as tables
from poker.tables import *
import sys
import poker.train
import poker


SERVER='ws://poker-dev.wrs.club:3001'

#SERVER='ws://atxholdem2.tplab.tippingpoint.com:3001'
PLAYERNAME = '9679095d66'
MODELNAME = 'basicPlayer'

def start_ai():
    cli = client.Client(SERVER, PLAYERNAME)
    cli.run()

if __name__ == "__main__":


    if "pull-tables" in sys.argv:
        tables.pull()
        print("Done")
        exit()
    elif "train" in sys.argv:
        poker.train.train()
        exit()

    parser = argparse.ArgumentParser(description='Launches AI poker player')
    parser.add_argument('-m', '--model', help='Model name for neural net', required=False, default=MODELNAME) 
    parser.add_argument('-p', '--player_name', help='Bot player name', required=False, default=PLAYERNAME) 
    parser.add_argument('-s', '--stats', help='Bot player name', action='store_true', required=False) 

    args = parser.parse_args()

    poker.ai.STATS = args.stats

    MODELNAME = args.model
    PLAYERNAME = args.player_name

    print(MODELNAME)
    load(MODELNAME)
    
    print(f"2 Players - K/K Unsuited - {win_chance(3, 'A', 'A', 'u')}")
    
    start_ai()
