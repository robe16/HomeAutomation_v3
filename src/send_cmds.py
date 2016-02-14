import urllib2
import telnetlib
import time
# import socket

def sendHTTP(ipaddress, connection, data=False, contenttype=False):
    if not ipaddress.startswith("http"):
        ipaddress = "http://" + ipaddress
    if data:
        req = urllib2.Request(ipaddress, data=data)
    else:
        req = urllib2.Request(ipaddress)
    if bool(contenttype):
        req.add_header("content-type", contenttype)
    req.add_header("Connection", connection)
    req.add_header("User-Agent","Linux/2.6.18 UDAP/2.0 CentOS/5.8")
    try:
        x = urllib2.urlopen(req, timeout=5)
        return False if not str(x.getcode()).startswith("2") else x
    except:
        return False

# Stopped working for unknown reason - sendTELNET added for use instead by tivo
# def sendSOCKET(ipaddress, port, data):
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.connect((ipaddress, port))
#         sock.send(bytes(data))
#         sock.close()
#         return True
#     except:
#         return False

def sendTELNET(ipaddress, port, data=None, response=False):
    try:
        tn = telnetlib.Telnet(ipaddress, port)
        time.sleep(0.1)
        output = tn.read_eager() if response else None
        if data:
            tn.write(str(data)+"\n")
            time.sleep(0.1)
            output = tn.read_eager()
            output = output if (response and not bool(output)) else True
        tn.close()
        return output
    except:
        return False