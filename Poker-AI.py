#!/usr/bin/python3
from poker import client
import poker.tables as tables
from poker.tables import *
import sys
import poker.train

SERVER='ws://poker-dev.wrs.club:3001'
PLAYERNAME = 'hamburger'

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

    if len(sys.argv) > 1:
        PLAYERNAME = sys.argv[1]

    print(f"2 Players - K/K Unsuited - {win_chance(3, 'A', 'A', 'u')}")
    
    start_ai()
