import websockets
from poker.ai import AI
import asyncio
import json
import hashlib

'''
Handle server events using the AI member functions below. The 'event' parameter is
the server-sent JSON already converted to a Python dictionary. The return value
should be the client response as a Python dictionary that will be converted to JSON
after it is returned
'''

class Client(object):

	def update_players(self, players_json):
		for obj in players_json:


	def _connect(self, event):
		obj = {"eventName" : "__join", "data" : {"playerName" : self.playername}}
		return obj

	def _new_peer(self, event):
		for player_name in event['data']:
			self.ai.get_player(player_name)

		return None

	def _start_reload(self, event):
		return {
			"eventName" : "__reload"
		}

	def _deal(self, event):
		return None

	def _action(self, event):
		return self.ai.request_action().to_json()

	def _bet(self, event):
		return self.ai.request_bet().to_json()

	def _show_action(self, event):
# update stuff
		return None

	def _round_end(self, event):
		return None

	def _game_over(self, event):
		return None

	def on_event(self, event):
		event_name = event["eventName"]
		handler = getattr(self, event_name[1:], None)
		if handler != None:
			return handler(event)
		print(f"Event {event_name} went unhandled!")
		return None

	def __init__(self, server, playername):
		self.server = server
		self.playername = playername
		md5 = hashlib.md5()
		md5.update(playername.encode('utf8'))
		md5 = md5.hexdigest()
		self.ai = AI(md5)
		print("Created player {} (MD5 {})".format(playername, md5))

	def log(self, sender, msg):
		log_msg = sender + ": " + msg + "\n"
		print(log_msg)
		with open(self.playername + "_log.txt", "a+") as log:
			log.write(log_msg)


	async def main_loop(self):
		async with websockets.connect(self.server) as sock:
			server_msg = '{"eventName" : "__connect"}'
			while(True):
				client_response = self.on_event(json.loads(server_msg))

				if client_response != None:
					client_response_txt = json.dumps(client_response)
					self.log("Client", client_response_txt)
					await sock.send(client_response_txt)

				server_msg = await sock.recv()
				self.log("Server", server_msg)

	def run(self):
		asyncio.get_event_loop().run_until_complete(self.main_loop())
			
