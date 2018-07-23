#!/usr/bin/python3
from poker import client
from poker.model import load
import argparse
import poker.tables as tables
from poker.tables import *
import sys
import poker.train

SERVER='ws://poker-dev.wrs.club:3001'
PLAYERNAME = 'hamburger'
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
    parser.add_argument('-m', '--model', help='Model name for neural net', required=False, defualt=MODELNAME) 
    parser.add_argument('-p', '--player_name', help='Bot player name', required=False, default=PLAYERNAME) 

    MODELNAME = args['model']
    PLAYERNAME = args['player_name']

    load(MODELNAME)
    
    print(f"2 Players - K/K Unsuited - {win_chance(3, 'A', 'A', 'u')}")
    
    start_ai()
