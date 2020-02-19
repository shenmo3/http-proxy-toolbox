from proxy import Proxy

if __name__ == '__main__':
    proxy_servers = []
    for port in [80]:
        temp = Proxy("0.0.0.0", "172.217.5.110", port)
        temp.start()
        proxy_servers.append(temp)
