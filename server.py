from threading import Thread, Event
import parser
import socket
import select
import random
import time
import importlib


class Server(Thread):
    def __init__(self, host, port, event, setting=None):
        super(Server, self).__init__()
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.connect((host, port))
        except:
            self.server = None
            print ("ERROR: failed to connect with unknown host ", host)
        self.client = None
        self.event = event
        self.shut = False
        self.setting = setting

    def run(self):
        delay = True
        while True:
            if self.shut:
                break
            if self.setting.server_msg:
                msg = self.setting.server_msg.encode("ISO-8859-1")
                self.setting.server_msg = ""
                self.client.sendall(msg)
                print("[==>] Proxy to server: ", msg)

            if not self.server:
                break
            r, w, e = select.select((self.server,), (), (), 0)
            if r:
                try:
                    data = self.server.recv(4096)
                    importlib.reload(parser)
                    data = parser.server_parser(data)
                    if data:
                        # delay
                        if delay:
                            time.sleep(
                                self.setting.delay + random.gauss(self.setting.jitter[0], self.setting.jitter[1]))
                            delay = False
                        # loss
                        if random.random() > self.setting.loss:
                            self.client.sendall(data)
                            print("[<==] Proxy sent back to client ", self.client)
                    else:
                        self.event.set()
                        break
                except:
                    # Server timeout
                    print ("[!] Server Timeout: connection reset by peer.")

            else:
                delay = True

        print("[*] Server closed")
