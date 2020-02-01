from threading import Thread
import socket


class Client(Thread):
	def __init__(self, host, port):
		super(Client, self).__init__()
		self.port = port
		self.host = host
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind((host, port))
		sock.listen(1)
		self.client, addr = sock.accept()

	def run(self):
		while True:
			pass
