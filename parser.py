def client_parser(data, port):
    print("client", port, "send:", data)
    return data


def server_parser(data, port):
    print("server", port, "send:", data)
    return data
