import socket
import time
import select
import matplotlib.pyplot as plt


def test():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = "0.0.0.0"
    port = 3456
    s.bind((host, port))
    s.listen(1)

    c, addr = s.accept()
    print ('Got connection from', addr)
    print ("Receiving...")

    start_time = time.time()
    l = c.recv(4096)
    while True:
        r,w,e = select.select((c,),(),(),0)
        if r:
            l = c.recv(4096)
            if not l:
                break
    t = time.time() - start_time
    print ("Done Receiving")
    c.close()
    return t


if __name__ == "__main__":
    x = []
    y = []
    for i in range(10):
        x.append(i + 1)
        y.append(test())
    plt.plot(x, y)
    plt.show()
