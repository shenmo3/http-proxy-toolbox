from threading import Thread
import socket


class Server(Thread):
	def __init__(self, host, port):
		super(Server, self).__init__()
		self.port = port
		self.host = host
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.connect((host, port))

	def run(self):
		while True:
			pass
