#!/usr/bin/env python3
import httprint
import tensorflow as tf
import sys

# Because tensorflow gave me errors when I put this further down
if '-o' in sys.argv:
	print("Eager mode!")
	tf.enable_eager_execution()

from poker import client
from poker.model import load
import argparse
from poker.lookup import *
import poker.train
import poker
import signal
from poker.ai import AI
from poker.ai.old import OldBot
from poker.ai.stat import StatBot, StatBot2
from poker.ai.qbot import QBot
from poker.ai.user import UserBot

# Constants!
PRACTICE_SERVER='ws://poker-dev.wrs.club:3001'
SERVER='ws://atxholdem2.tplab.tippingpoint.com:3001' 

SERVERS = {
	'server': SERVER,
	'practice': PRACTICE_SERVER 
}

PLAYER_NAME = '9679095d66'

DEFAULT_OLD_MODEL = 'basicPlayer1'

# Entry point
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Launches AI poker player')

	# Positional arguments
	parser.add_argument('env', metavar='Environment', type=str, help='(server|practice|roomai)')
	parser.add_argument('bot', metavar='Bot', type=str, help='(bot|stats|stats2|qbot)')

	# Optional arguments
	parser.add_argument('-n', '--name', help='Bot player name on server', required=False, default=PLAYER_NAME) 
	parser.add_argument('-l', '--load', help='Load model name', required=False, default=None)
	parser.add_argument('-s', '--save', help='Save model name', required=False, default=None)
	parser.add_argument('-v', '--version', help='Model version for regular bot', type=int, required=False, default=0)
	parser.add_argument('-p', '--port', help='Port for console output (If set, connect to http://<ip>:<port> for console output)', type=int, required=False, default=-1)
	parser.add_argument('-e', '--eps', help='Starting EPS for QBot', type=float, required=False, default=0.5)

	args = parser.parse_args()

	# Create bot
	if args.bot == 'bot':
		model_name = args.load or DEFAULT_OLD_MODEL
		ai = OldBot(model_name, args.version)
	elif args.bot == 'stats2':
		ai = StatBot2()
	elif args.bot == 'user':
		ai = UserBot()
	elif args.bot == 'qbot':
		ai = QBot(load=args.load, eps=args.eps)

	# Setup remote console output
	if args.port != -1:
		httprint.init(port=args.port)
		httprint.set_global_title(ai.name)

	print(f'Created {ai.name}!')
	
	# Save model on exit
	def exit_gracefully(signum=None, frame=None):
		print("Exiting Gracefully!")
		if args.save != None:
			ai.save_model(args.save)
			print(f"Saved model to {args.save}")
		exit()

	signal.signal(signal.SIGINT, exit_gracefully)
	signal.signal(signal.SIGTERM, exit_gracefully)

	# Start environment
	if args.env == 'roomai':
		poker.train.train(ai)
		exit_gracefully()
	elif args.env in ('server', 'practice'):
		server = SERVERS[args.env]
		cli = client.Client(server, args.name, ai)
		cli.run()
