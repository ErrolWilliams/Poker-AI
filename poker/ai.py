# Handle server events using the AI member functions below. The 'event' parameter is
# the server-sent JSON already converted to a Python dictionary. The return value
# should be the client response as a Python dictionary that will be converted to JSON
# after it is returned.

class AI(object):

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
# action goes here!
		return None

	def _bet(self, event):
		return {
			"eventName" : "__action",
			"data" : {
				"action" : "bet",
				"amount" : 0
			}
		}

	def _show_action(self, event):
		return None

	def _round_end(self, event):
		return None

	def _game_over(self, event):
		return None

	def __init__(self, playername):
		self.playername = playername
		print("Created player {}".format(playername))

	def on_event(self, event):
		event_name = event["eventName"]
		handler = getattr(self, event_name[1:], None)
		if handler != None:
			return handler(event)
		print(f"Event {event_name} went unhandled!")
		return None

