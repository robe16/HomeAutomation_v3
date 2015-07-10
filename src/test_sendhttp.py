import urllib2
import httplib

from src.cmd_http import sendHTTP


def testHTTP(ipaddress, path, connection, expected, port=None, data=""):
    if port==None:
        url = ipaddress
        x = sendHTTP(ipaddress, path, connection, data=data)
    else:
        url = ipaddress+":"+port
        x = sendHTTP(ipaddress, path, connection, data=data, port=port)
    print (url+path)

    if expected and x!=False:
        print ("Test Result: PASS")
    elif expected==x:
        print ("Test Result: PASS")
    else:
        print ("Test Result: FAIL")


print ("**** Test 1: Google & /search ****")
testHTTP("https://www.google.co.uk", "/search", "close", True)

print ("**** Test 2: Internal IP with port number ****")
testHTTP("http://192.168.0.100", "/web/index.html", "close", True, port="32400")

print ("**** Test 3: Redirect ****")
testHTTP("http://steamcommunity.com", "/id/robe_16/home/", True, "close")

print ("**** Test 4: Intentional HTTP Fail ****")
testHTTP("https://www.google.co.uk", "/asdfg", "close", False)

print ("**** Test 5: 'http://' correction ****")
testHTTP("www.google.co.uk", "/search", "close", True)
