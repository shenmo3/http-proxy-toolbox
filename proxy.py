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
            print("[%]Waiting for connection on:", self.client_port)
            self.client = Client(self.from_host, self.client_port, self.event, self.setting)
            if (self.to_host != "0.0.0.0"):
                self.server = Server(self.to_host, self.server_port, self.event, self.setting)
                print("[*]Connection established on client:" + str(self.client_port) + ", and server: " + str(self.to_host))
            else:
                print (("[*]Connection established on:", self.client_port))

            if self.client.addr in self.setting.acl:
                if not self.setting.acl[self.client.addr]:
                    self.client = None
                    self.server = None
                    print("[!]Connection", self.client.addr, "terminated by ACL")
                    continue
            elif not self.setting.acl["default"]:
                self.client = None
                self.server = None
                print("[!]Connection", self.client.addr, "terminated by default ACL")
                continue

            if (self.to_host != "0.0.0.0"):
                self.client.server = self.server.server
                self.server.client = self.client.client
                self.client.start()
                self.server.start()
                self.event.wait()
                if self.server.is_alive():
                    self.server.shut = True
                if self.client.is_alive():
                    self.client.shut = True
            # Parse the client request and set server
            else:
                webserver, port = self.client.get_request()
                # Shut down the server if parse not successfully
                if (webserver == -1) and (port == -1):
                    if self.server and self.server.is_alive():
                        self.server.shut = True
                    if self.client and self.client.is_alive():
                        self.client.shut = True
                    self.event.wait()
                    break
                else:
                    self.server = Server(webserver, port, self.event, self.setting)
                    if self.server.server:
                        print("[*]Connection established on client:" + str(self.client_port) + ", and server: " + str(webserver))
                    self.client.server = self.server.server
                    self.server.client = self.client.client
                    print ("[*]Client.server: ",self.client.server)
                    print ("[*]Server.client: ", self.server.client)
                    self.client.start()
                    self.server.start()
                    self.event.wait()
                    if self.server.is_alive():
                        self.server.shut = True
                    if self.client.is_alive():
                        self.client.shut = True
