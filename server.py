from threading import Thread, Event
import socket
import select


class Server(Thread):
    def __init__(self, host, port, event):
        super(Server, self).__init__()
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        self.client = None
        self.event = event
        self.shut = False

    def run(self):
        while True:
            if self.shut:
                break
            r, w, e = select.select((self.server,), (), (), 0)
            if r:
                data = self.server.recv(4096)
                print("server receive: ", data)
                if data:
                    self.client.sendall(data)
                else:
                    self.event.set()
                    break
        print("server closed")
