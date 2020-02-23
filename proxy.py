import socket
import threading

from setting import Setting
from threading import Thread, Event
from utilities import *


class Proxy(Thread):
    def __init__(self,local_host, local_port, setting):
        super(Proxy, self).__init__()

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((local_host,local_port))

        self.serverSocket.listen(10)  # become a server socket
        self.__clients = {}
        self.setting = setting


    def setSetting(self, setting):
        self.setting = setting


    def feature_trigger(self):
        # Add delay to package transmission
        if self.setting.delay:
            print ("Add delay " + str(self.setting.delay) + "s")
            time.sleep(self.setting.delay)

        # Add jitter between packages transmission
        if self.setting.jitter:
            jitter = random.random() * 10
            print ("Add jitter " + str(jitter) + "s")
            time.sleep(jitter)

        # Simulate data loss
        if random.random() < self.setting.loss:
            return False

        return True


    def package_process(self, client_socket, client_addr):
        # Step1: handle the request from the client
        # parse the url to get info on webserver , the port

        client_socket.settimeout(self.setting.connection_timeout)
        try:
            origin_request = client_socket.recv(self.setting.pkg_size)
        except:
            print ("Client connection time out: " + str(client_socket))
            print (client_socket)
            client_socket.close()
            return

        webserver, port = requset_handler(origin_request)
        # Url parse error
        if (webserver == -1) and (port == -1):
            client_socket.close()
            return

        # TODO: add black and white list functionality
        result = self.feature_trigger()
        # Package loss
        if not result:
            print ("[!]Package from client loss")
            print ("[!]Close client connection")
            client_socket.close()
            return

        try:
            # create a socket to connect to the web server
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #server_socket.settimeout(self.setting.connection_timeout)
            server_socket.connect((webserver, port))  # connecting to the server using url and port

            server_socket.sendall(origin_request)  # send request to webserver
            print("[==>] Sent to server\n")

            while True:
                # receive data from web server as reply to request
                data = server_socket.recv(self.setting.pkg_size)
                if (len(data) > 0):
                    print ("\n[<==]Get back package from server " + webserver + ", package size: " + str(len(data)))
                    print ("[<==]Package should be sent back to " + str(client_socket))
                    print(data)

                    # TODO: add black and white list functionality
                    result = self.feature_trigger()
                    # Package loss
                    if result:
                        client_socket.send(data)  # send data back to client
                        print("[<==] Sent to localhost.\n")
                    else:
                        print ("[!]Package from server loss")

                else:
                    print("[*] No more data. Close " + str(client_socket) + " Connections.")
                    break

            server_socket.close()
            client_socket.close()


        except socket.error as error_msg:
            print ('ERROR: ', client_addr, error_msg)
            if server_socket:
                server_socket.close()
            if client_socket:
                client_socket.close()


    def run(self):
        while True:
            # Estabish the connection, accept the incoming request to the socket
            (client_socket,client_address) = self.serverSocket.accept()
            print("[==>] Received incoming connection from  " + str(client_socket))

            d = threading.Thread(target = self.package_process,
                                 args=(client_socket, client_address) )
            d.setDaemon(True)
            d.start()


    def shutdown(self, signum, frame):
        """ Handle the exiting server. Clean all traces """
        self.serverSocket.close()
        sys.exit(0)
