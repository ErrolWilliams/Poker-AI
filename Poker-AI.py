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
import signal


TEST_SERVER='ws://poker-dev.wrs.club:3001'
SERVER='ws://atxholdem2.tplab.tippingpoint.com:3001' 

PLAYERNAME = '9679095d66'
MODELNAME = 'basicPlayer'


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
	parser.add_argument('--stats', '--stats', help='Bot player name', action='store_true', required=False) 
	parser.add_argument('-t', '--test', help='Use test server', action='store_true', required=False)
	parser.add_argument('-l', '--load', help='Load model', required=False, default=None)
	parser.add_argument('-s', '--save', help='Save model', required=False, default=None)
	parser.add_argument('-o', '--old', help='Old models', required=False, action='store_true')
	

	args = parser.parse_args()

	

	ai = poker.ai.AI()

	ai.OLD = args.old

	if args.load != None:
		ai.load_model(args.load)
	else:
		ai.create_model()

	def exit_gracefully(signum, frame):
		print("Exiting Gracefully!")
		if args.save != None:
			ai.save_model(args.save)
			print(f"Saved model to {args.save}")
		exit()

	signal.signal(signal.SIGINT, exit_gracefully)
	signal.signal(signal.SIGTERM, exit_gracefully)
	
	poker.ai.STATS = args.stats

	if args.test:
		SERVER = TEST_SERVER

	MODELNAME = args.model
	PLAYERNAME = args.player_name

	print(MODELNAME)
	load(MODELNAME)
	
	cli = client.Client(SERVER, PLAYERNAME, ai)
	cli.run()
