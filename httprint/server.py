from http import server
import threading
import time
from os import path
import json

_main_server = None

class _Handler(server.BaseHTTPRequestHandler):

	def __init__(self, request, client_address, server):
		super().__init__(request, client_address, server)

	def do_POST(self):
		return _main_server.post(self)
	
	def do_GET(self):
		return _main_server.get(self)

	def log_message(self, format, *args):
		return



class _Server(threading.Thread):

	def __init__(self, port=8000, global_title='HTTPrint'):
		super().__init__()
		self.port = port
		self.global_title = global_title
		self.log = []

	def index(self, handler):
		handler.send_response(200)
		handler.send_header('Content-type', 'text/html')
		handler.end_headers()
		with open(path.join(path.dirname(__file__),'index.html'), 'rb') as f:
			handler.wfile.write(f.read())

	def ajax(self, handler):
		timestamp = float(handler.path.split('/')[-1])

		to_send = None

		log_len = len(self.log)
		min_i = log_len - 2000

		for i in range(log_len - 1, -1, -1):
#print(self.log[i]['timestamp'])
#			print("vs")
#			print(timestamp)
			if self.log[i]['timestamp'] <= timestamp or i < min_i:
				to_send = self.log[(i+1):log_len]
				break

		if to_send == None:
			to_send = self.log[0:log_len]

		if len(to_send) > 0:
			timestamp = to_send[-1]['timestamp']

		obj = {'lastTimestamp': timestamp, 'log': to_send, 'globalTitle': self.global_title}

		handler.send_response(200)
		handler.send_header('Content-type', 'text/html')
		handler.end_headers()
		handler.wfile.write(json.dumps(obj).encode('utf-8'))

	def get(self, handler):
		if handler.path.startswith('/ajax'):
			return self.ajax(handler)
		return self.index(handler)

	def post(self, handler):
		return
	
	def append(self, text, id=0):
		self.log.append({'timestamp': time.time(), 'id': id, 'text': text})

	def run(self):
		global _main_server
		_main_server = self
		addr = ('', self.port)
		self.httpd = server.HTTPServer(addr, _Handler)
		self.httpd.serve_forever()

