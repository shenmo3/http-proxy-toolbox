import socket
import time
import matplotlib.pyplot as plt


def test():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "0.0.0.0"
    port = 3456
    s.connect((host, port))

    print("Sending...")

    with open("filename", "r") as f:
        start_time = time.time()
        s.sendall(f.read().encode("ISO-8859-1"))
        t = time.time() - start_time
        print("Done Sending")
    s.close()
    return t


if __name__ == "__main__":
    x = []
    y = []
    for i in range(10):
        x.append(i + 1)
        y.append(test())
    plt.plot(x, y)
    plt.show()
