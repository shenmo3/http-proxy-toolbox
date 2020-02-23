import socket
import sys
import os

from proxy import Proxy
from setting import Setting
from utilities import *


def main():
    # Handle user input
    if len(sys.argv[1:]) != 2 :
        print("Usage: python3 proxy.py [localhost] [localport]")
        print("Example: python3 proxy.py 127.0.0.1 12345")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    setting = Setting()
    proxy_servers = []

    #TODO: setting feature toggle for performance
    temp = Proxy(local_host, local_port, setting)
    temp.start()
    proxy_servers.append(temp)

    while True:
        cmd = ""
        try:
            changed = True
            cmd = input("\n% Add feature here: ").split()
            if cmd[0] == "exit":
                os._exit(0)
            elif cmd[0] == "loss":
                setting.loss = int(cmd[1])
                print("[*]loss set to", setting.loss)
            elif cmd[0] == "delay":
                setting.delay = int(cmd[1])
                print("[*]delay set to ", setting.delay)
            elif cmd[0] == "jitter":
                setting.jitter = int(cmd[1])
                print("[*]jitter set to ", setting.jitter)
            elif cmd[0] == "blacklist":
                if len(cmd) == 3 and cmd[1] == '-d':
                    if cmd[2] in setting.black_list:
                        setting.black_list.remove(cmd[2])
                        print ("[*]delete " + cmd[2] + " from black list")
                    else:
                        print ("[!] " + cmd[2] + " not in black list now")
                else:
                    if cmd[1] not in setting.black_list:
                        setting.black_list.append(cmd[1])
                        print("[*]black list set to ", setting.black_list)
                    else:
                        print ("[!] " + cmd[1] + " already in black list now")
            elif cmd[0] == "whitelist":
                if len(cmd) == 3 and cmd[1] == '-d':
                    if cmd[2] in setting.white_list:
                        setting.white_list.remove(cmd[2])
                        print ("[*]delete " + cmd[2] + " from white list")
                    else:
                        print ("[!] " + cmd[2] + " not in white list now")
                else:
                    if cmd[1] not in setting.white_list:
                        setting.white_list.append(cmd[1])
                        print("[*]white list set to ", setting.white_list)
                    else:
                        print ("[!] " + cmd[1] + " already in white list now")
            else:
                print("[!]Unknown command:", cmd)
                changed = False

            if len(cmd) > 0 and changed:
                temp.setSetting(setting)

        except Exception as e:
            print("[!]Unknown command:", "".join(cmd))


if __name__ == "__main__":
    welcome_message()
    main()
