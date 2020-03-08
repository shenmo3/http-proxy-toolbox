from threading import Thread, Event
import parser
import socket
import select
import random
import time
import importlib


class Client(Thread):
    def __init__(self, host, port, event, setting=None):
        super(Client, self).__init__()
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        self.client, self.addr = sock.accept()
        self.server = None
        self.event = event
        self.shut = False
        self.setting = setting

    def run(self):
        try:
            delay = True
            while True:
                if self.shut:
                    self.client.close()
                    break
                if self.setting.client_msg:
                    msg = self.setting.client_msg.encode("ISO-8859-1")
                    self.setting.client_msg = ""
                    self.server.sendall(msg)
                    print("proxy -> client: ", msg)
                r, w, e = select.select((self.client,), (), (), 0)
                if r:
                    data = self.client.recv(4096)
                    try:
                        importlib.reload(parser)
                        data = parser.client_parser(data, self.port)
                    except Exception as e:
                        print("client parser error", self.port, e)
                    if data:
                        # delay
                        if delay:
                            time.sleep(self.setting.delay + random.gauss(self.setting.jitter[0], self.setting.jitter[1]))
                            delay = False
                        # loss
                        if random.random() > self.setting.loss:
                            self.server.sendall(data)
                    else:
                        self.event.set()
                        break
                else:
                    delay = True
            print("client closed")
        except Exception as e:
            print("client", self.port, e)
            self.event.set()
