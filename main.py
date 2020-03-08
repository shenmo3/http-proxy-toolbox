from proxy import Proxy
from setting import Setting
import os

if __name__ == '__main__':
    setting = Setting()
    proxy_servers = []
    for port in [80]:
        # TODO: setting feature toggle for performance
        temp = Proxy("0.0.0.0", "0.0.0.0", port, 3456, setting)
        temp.start()
        proxy_servers.append(temp)

    while True:
        cmd = ""
        try:
            cmd = input("% ").split()
            if cmd[0] == "quit":
                os._exit(0)
            elif cmd[0] == "C":
                setting.client_msg += " ".join(cmd[1:]) + "\r\n"
            elif cmd[0] == "S":
                setting.server_msg += " ".join(cmd[1:]) + "\r\n"
            elif cmd[0] == "loss":
                setting.loss = int(cmd[1])
                print("loss set to ", setting.loss)
            elif cmd[0] == "delay":
                setting.delay = int(cmd[1])
                print("delay set to ", setting.delay)
            elif cmd[0] == "jitter":
                setting.jitter[0] = int(cmd[1])
                setting.jitter[1] = int(cmd[2])
                print("jitter set to ", setting.jitter)
            elif cmd[0] == "acl":
                if cmd[1] == "add" or cmd[1] == "-a":
                    setting.acl[cmd[2]] = (cmd[3] == "accept")
                    print("acl entry added: ", cmd[2], "->", setting.acl[cmd[2]])
                elif cmd[1] == "delete" or cmd[1] == "-d":
                    if cmd[2] != "default":
                        del setting.acl[cmd[2]]
                        print("acl entry deleted: ", cmd[2])
                    else:
                        print("you cannot delete the default acl, you can only use add to set it.")
                elif cmd[1] == "show":
                    print(setting.acl)
                else:
                    raise Exception("Unknown ACL sub-command")
            else:
                print("Unknown command:", cmd)
        except Exception as e:
            print("Unknown command:", "".join(cmd))
            print(e)
