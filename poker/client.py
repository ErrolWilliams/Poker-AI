import websockets
from poker.ai import AI
import asyncio
import json

class Client(object):
	def __init__(self, server, playername):
		self.server = server
		self.ai_player = AI(playername)


	async def main_loop(self):
		async with websockets.connect(self.server) as sock:
			server_msg = '{"eventName" : "__connect"}'
			while(True):
				client_response = self.ai_player.on_event(json.loads(server_msg))

				if client_response != None:
					await sock.send(json.dumps(client_response))

				server_msg = await sock.recv()

	def run(self):
		asyncio.get_event_loop().run_until_complete(self.main_loop())
			
