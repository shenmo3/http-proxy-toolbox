from threading import Thread, Event
import socket
import select


class Client(Thread):
    def __init__(self, host, port, event):
        super(Client, self).__init__()
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        self.client, addr = sock.accept()
        self.server = None
        self.event = event
        self.shut = False

    def run(self):
        while True:
            if self.shut:
                break
            r, w, e = select.select((self.client,), (), (), 0)
            if r:
                data = self.client.recv(4096)
                print("client receive: ", data)
                if data:
                    self.server.sendall(data)
                else:
                    self.event.set()
                    break
        print("client closed")
