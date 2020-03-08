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
        self.server.connect((host, port))
        self.client = None
        self.event = event
        self.shut = False
        self.setting = setting

    def run(self):
        try:
            delay = True
            while True:
                if self.shut:
                    self.server.close()
                    break
                if self.setting.server_msg:
                    msg = self.setting.server_msg.encode("ISO-8859-1")
                    self.setting.server_msg = ""
                    self.client.sendall(msg)
                    print("proxy -> server: ", msg)
                r, w, e = select.select((self.server,), (), (), 0)
                if r:
                    data = self.server.recv(4096)
                    try:
                        importlib.reload(parser)
                        data = parser.server_parser(data, self.port)
                    except Exception as e:
                        print("server parser error", self.port, e)
                    if data:
                        # delay
                        if delay:
                            time.sleep(self.setting.delay + random.gauss(self.setting.jitter[0], self.setting.jitter[1]))
                            delay = False
                        # loss
                        if random.random() > self.setting.loss:
                            self.client.sendall(data)
                    else:
                        self.event.set()
                        break
                else:
                    delay = True
            print("server closed")
        except Exception as e:
            print("server", self.port, e)
            self.event.set()
