#!/usr/bin/python3
import httprint
import tensorflow as tf
import sys

if '-o' in sys.argv:
	print("Eager mode!")
	tf.enable_eager_execution()

from poker import client
from poker.model import load
import argparse
import poker.tables as tables
from poker.tables import *
import poker.train
import poker
import signal
from poker.ai import AI, OldBot, StatBot, StatBot2, QBot, UserBot


TEST_SERVER='ws://atxholdem.tplab.tippingpoint.com:3001'
SERVER='ws://atxholdem2.tplab.tippingpoint.com:3001' 

PLAYERNAME = '9679095d66'
DEFAULT_MODEL = 'basicPlayer1'

if __name__ == "__main__":

	if "pull-tables" in sys.argv:
		tables.pull()
		print("Done")
		exit()
	elif "train" in sys.argv:
		poker.train.train()
		exit()

	parser = argparse.ArgumentParser(description='Launches AI poker player')
	parser.add_argument('-m', '--model', help='Model name for neural net', required=False, default=DEFAULT_MODEL) 
	parser.add_argument('-p', '--player_name', help='Bot player name', required=False, default=PLAYERNAME) 
	parser.add_argument('--stats', '--stats', help='Bot player name', action='store_true', required=False) 
	parser.add_argument('-t', '--test', help='Use test server', action='store_true', required=False)
	parser.add_argument('-l', '--load', help='Load model', required=False, default=None)
	parser.add_argument('-s', '--save', help='Save model', required=False, default=None)
	parser.add_argument('-o', '--old', help='Old models', required=False, action='store_true')
	parser.add_argument('-r', '--roomai', help='Use RoomAI', required=False, action='store_true')
	parser.add_argument('-v', '--version', help='Model Version', type=int, required=False, default=0)
	parser.add_argument('-u', '--user', help='Use user input', required=False, action='store_true')
	parser.add_argument('--port', '--port', help='Port for console output', type=int, required=False, default=-1)

	args = parser.parse_args()

	if args.port != -1:
		httprint.init(port=args.port)

	ai = None

	if args.old:
		ai = OldBot(args.model, args.version)
		print(f"Creating OldBot with model {args.model}")
	elif args.stats:
		ai = StatBot2()
		print("Creating StatBot")
	elif args.user:
		ai = UserBot()
	else:
		ai = QBot()
		print("Creating QBot")
		if args.load != None:
			ai.load_model(args.load)
		else:
			ai.create_model()

	server = TEST_SERVER if args.test else SERVER
	playername = args.player_name
	
	def exit_gracefully():
		print("Exiting Gracefully!")
		if args.save != None:
			ai.save_model(args.save)
			print(f"Saved model to {args.save}")
		exit()

	signal.signal(signal.SIGINT, lambda signum, frame: exit_gracefully())
	signal.signal(signal.SIGTERM, lambda signum, frame: exit_gracefully())

	if args.roomai:
		poker.train.train(ai)
		exit_gracefully()
	else:
		cli = client.Client(server, playername, ai)
		cli.run()
