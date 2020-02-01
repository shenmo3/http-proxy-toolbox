from server import Server
from client import Client
from threading import Thread


class Proxy(Thread):
	def __init__(self, from_host, to_host, port):
		super(Proxy, self).__init__()
		print("waiting for connection on:", port)
		self.client = Client(from_host, port)
		self.server = Server(to_host, port)
		print("connection established on:", port)
