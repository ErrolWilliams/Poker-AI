#!/usr/bin/python3
from poker import client
import poker.tables as tables
from poker.tables import *
import sys

SERVER='ws://poker-dev.wrs.club:3001'
PLAYERNAME = 'test1595'

def start_ai():
    cli = client.Client(SERVER, PLAYERNAME)
    cli.run()

if __name__ == "__main__":

    if "pull-tables" in sys.argv:
        tables.pull()
        print("Done")
        exit()


    print(f"2 Players - K/K Unsuited - {win_chance(2, 'K', 'K', 'u')}")
    
    start_ai()
