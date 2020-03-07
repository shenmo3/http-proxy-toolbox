from proxy import Proxy
from setting import Setting
import os

if __name__ == '__main__':
    setting = Setting()
    proxy_servers = []
    for port in [80]:
        # TODO: setting feature toggle for performance
        temp = Proxy("0.0.0.0", "172.217.5.110", port, 3456, setting)
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
            elif cmd[0] == "blacklist":
                setting.black_list.append(cmd[1])
                print("black list set to ", setting.black_list)
            elif cmd[0] == "whitelist":
                setting.white_list.append(cmd[1])
                print("white list set to ", setting.white_list)
            # TODO: delete from list
            else:
                print("Unknown command:", cmd)
        except Exception as e:
            print("Unknown command:", "".join(cmd))
