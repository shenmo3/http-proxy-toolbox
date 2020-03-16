import time
import random

from setting import Setting


def requset_handler(origin_request):
    request = origin_request.decode("utf-8")
    # parse the first line
    first_line = request.split('\n')[0]
    # print ()
    # print ("First line of request is " + first_line)

    # get url
    try:
        url = first_line.split(' ')[1]
        #print (url)
    except:
        print ("Parse error happens.")
        print ("Failed to parse:",first_line.split(' '))
        return (-1, -1)

    # find the webserver and port
    http_pos = url.find("://")  # find pos of ://

    if (http_pos == -1):
        temp = url
    else:
        # get the rest of url
        temp = url[(http_pos + 3):]
        # print("reqd_url:", temp)

    # find the port pos (if any) =>returns -1 if none found
    port_pos = temp.find(":")

    # find end of web server=> if / not found it is just set as length of the reqd_url
    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)

    webserver = ""
    port = -1

    if (port_pos == -1 or webserver_pos < port_pos):  # Use default http port: 80
        port = 80
        webserver = temp[:webserver_pos]
    else:  # specific destination port
        port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
        webserver = temp[:port_pos]

    print("[==>] Final_web_server:", webserver, "Port:", port)

    return (webserver, port)
