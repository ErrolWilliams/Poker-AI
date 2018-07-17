from poker import client
import tables
from tables import *
import sys

def start_ai():
    cli = client.Client('ws://poker-dev.wrs.club:3001', 'TEAM_JE')
    cli.run()

if __name__ == "__main__":

    if "pull-tables" in sys.argv:
        tables.pull()
        print("Done")
        exit()


    print(f"2 Players - K/K Unsuited - {win_chance(2, 'K', 'K', 'u')}")
    
    start_ai()
