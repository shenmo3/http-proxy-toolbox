from server import Server
from client import Client
from threading import Thread, Event


class Proxy(Thread):
    def __init__(self, from_host, to_host, server_port, client_port, setting=None):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.server_port = server_port
        self.client_port = client_port
        self.client = None
        self.server = None
        self.event = Event()
        self.setting = setting

    def run(self):
        while True:
            self.event.clear()
            print("waiting for connection on:", self.client_port)
            self.client = Client(self.from_host, self.client_port, self.event, self.setting)
            self.server = Server(self.to_host, self.server_port, self.event, self.setting)
            print("connection established on:", self.client_port)
            if self.client.addr in self.setting.acl:
                if not self.setting.acl[self.client.addr]:
                    self.client = None
                    self.server = None
                    print("connection", self.client.addr, "terminated by ACL")
                    continue
            elif not self.setting.acl["default"]:
                self.client = None
                self.server = None
                print("connection", self.client.addr, "terminated by default ACL")
                continue
            self.client.server = self.server.server
            self.server.client = self.client.client
            self.client.start()
            self.server.start()
            self.event.wait()
            if self.server.is_alive():
                self.server.shut = True
            if self.client.is_alive():
                self.client.shut = True
