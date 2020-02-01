from proxy import Proxy


if __name__ == '__main__':
	proxy_servers = []
	for port in [1000]:
		temp = Proxy("0.0.0.0", "0.0.0.0", port)
		temp.start()
		proxy_servers.append(temp)

	while True:
		pass
