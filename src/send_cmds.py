from  urllib2 import Request, urlopen, HTTPError
import telnetlib
import time
from console_messages import print_error, print_http
# import socket

def sendHTTP(url1, connection, url2='', data=False, contenttype=False, header_auth=False, redirect=0):
    #
    if redirect >= 5:
        return False
    #
    url = _check_prefix(url1) + url2
    #
    if data:
        req = Request(url, data=data)
    else:
        req = Request(url)
    #
    if bool(contenttype):
        req.add_header("content-type", contenttype)
    #
    if bool(header_auth):
        req.add_header("Authorization", header_auth)
    #
    req.add_header("Connection", connection)
    req.add_header("User-Agent","Linux/2.6.18 UDAP/2.0 CentOS/5.8")
    #
    try:
        x = urlopen(req, timeout=10)
        return False if not str(x.getcode()).startswith("2") else x
    except HTTPError as h:
        if str(h.getcode()).startswith("3"):
            print_http(h.getcode(), 'Redirect of http request - ' + str(h))
            url_redirect = h.headers['Location']
            return sendHTTP(url_redirect, connection, data=data, contenttype=contenttype, header_auth=header_auth, redirect=redirect+1)
        else:
            print_http(h.getcode(), 'Could not send http request - ' + str(h))
        return False
    except Exception as e:
        print_error('Could not send http request - ' + str(e))
        return False

def _check_prefix(url):
    if not url.startswith("http"):
        return "http://" + url
    else:
        return url


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