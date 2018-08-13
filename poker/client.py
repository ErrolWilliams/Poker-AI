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
		for player_json in players_json:
			self.ai.get_player(player_json['playerName']).json_update(player_json)

	def update_table(self, table_json):
		self.ai.table.json_update(table_json)


	def _connect(self, event):
		obj = {"eventName" : "__join", "data" : {"playerName" : self.playername}}
		return obj

	def _game_prepare(self, event):
		countdown = event['data']['countDown']
		if countdown == 5:
			print("Game starting in")
		print(countdown)

	def _new_round(self, event):
		table_num = event['data']['table']['tableNumber']
		table_url = 'http://{}/game.html?table={}'.format(self.server, table_num)
		print(table_url)
		
#update_players(self, event['data']['players'])
		return None

	def _left(self, event):
		new = {}
		for player in self.ai.table.players:
			if player in event['data']:
				new[player] = self.ai.table.players[player]
			else:
				print(f"Deleted {player}")
		self.ai.table.players = new

	def _new_peer(self, event):
		for player_name in event['data']:
			self.ai.get_player(player_name)

		return None

	def _new_peer_2(self, event):
		print('ay lemao')

	def _start_reload(self, event):
		return {
			"eventName" : "__reload"
		}

	def _deal(self, event):
		self.update_table(event['data']['table'])
		self.update_players(event['data']['players'])
#	update_players(self, event['data']['players'])
		return None

	def _action(self, event):
		self.update_table(event['data']['game'])
		self.update_players(event['data']['game']['players'])
		self.ai.player.json_update(event['data']['self'])
		return self.ai.request().to_json()

	def _bet(self, event):
		return self.ai.request_bet().to_json()

	def _show_action(self, event):
		self.update_table(event['data']['table'])
		self.update_players(event['data']['players'])
		return None

	def _round_end(self, event):
		self.update_table(event['data']['table'])
		self.update_players(event['data']['players'])
		self.ai.round_end()
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

	def __init__(self, server, playername, ai):
		self.ai = ai
		self.server = server
		self.playername = playername
		md5 = hashlib.md5()
		md5.update(playername.encode('utf8'))
		md5 = md5.hexdigest()
		self.ai.attach(md5)
		print("Created player {} (MD5 {})".format(playername, md5))

	def log(self, sender, msg):
		# No fcntl on Windows... will silently fail
		try:
			import fcntl
			log_msg = f"[{self.playername}] from {sender} : {msg}\n"
			with open("client_log.txt", "a+") as log:
				fcntl.flock(log, fcntl.LOCK_EX)
				log.write(log_msg)
				fcntl.flock(log, fcntl.LOCK_UN)
		except Error as e:
			pass


	async def main_loop(self):
		print(self.server)
		while(True):
			try:
				async with websockets.connect('ws://{}'.format(self.server)) as sock:
					server_msg = '{"eventName" : "__connect"}'
					while(True):
						client_response = self.on_event(json.loads(server_msg))

						if client_response != None:
							client_response_txt = json.dumps(client_response)
							print(client_response_txt)
							self.log("Client", client_response_txt)
							await sock.send(client_response_txt)

						server_msg = await sock.recv()
						self.log("Server", server_msg)
			except ConnectionRefusedError as e:
				print("Connection refused... retrying")

	def run(self):
		asyncio.get_event_loop().run_until_complete(self.main_loop())
			
