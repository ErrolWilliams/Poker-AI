import websockets
from poker.ai import AI
import asyncio
import json

'''
Handle server events using the AI member functions below. The 'event' parameter is
the server-sent JSON already converted to a Python dictionary. The return value
should be the client response as a Python dictionary that will be converted to JSON
after it is return
'''

class Client(object):

	def _connect(self, event):
		obj = {"eventName" : "__join", "data" : {"playerName" : self.playername}}
		return obj

	def _new_peer(self, event):
		print("New peer!")
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

	def __init__(self, playername):
		self.playername = playername
		self.ai = AI()
		print("Created player {}".format(playername))

	async def main_loop(self):
		async with websockets.connect(self.server) as sock:
			server_msg = '{"eventName" : "__connect"}'
			while(True):
				client_response = self.on_event(json.loads(server_msg))

				if client_response != None:
					await sock.send(json.dumps(client_response))

				server_msg = await sock.recv()

	def run(self):
		asyncio.get_event_loop().run_until_complete(self.main_loop())
			
