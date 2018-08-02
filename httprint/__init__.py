# Written By: Coleman Dill
# Last Change: 27 July 2018

import sys
from .server import _Server
from urllib import request, parse


class _ExternalServer(object):
	def __init__(self):
		pass



def init(port=8000, is_host=None):

	server = _Server(port)
	server.start()

	old_print = sys.stdout.write
	old_err = sys.stderr.write

	def new_print(text):
		server.append(text)
		old_print(text)

	def new_err(text):
		server.append(text)
		old_err(text)
		
	sys.stdout.write = new_print
	sys.stderr.write = new_err
	
