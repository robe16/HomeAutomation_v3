from cmd_http import sendHTTP
import urllib2
import httplib


def testHTTP(ipaddress, path, connection, port=None, data=""):
    if port==None:
        url = ipaddress
    else:
        url = ipaddress+":"+port
    print (url+path)
    x = sendHTTP(url, path, connection, data)

    if type(x)==httplib.HTTPResponse and str(x.getcode()).startswith("2"):
        print ("Test Result: PASS")
    elif type(x)==urllib2.HTTPError:
        print ("Test Result: FAIL - "+str(x.code)+" "+str(x.reason))
    elif type(x)==urllib2.URLError:
        print ("Test Result: FAIL - "+str(x.reason))
    else:
        print ("Error")


print ("**** Test 1: Google & /search ****")
testHTTP("https://www.google.co.uk", "/search", "close")

print ("**** Test 2: Internal IP with port number ****")
testHTTP("http://192.168.0.100", "/web/index.html", "close", port="32400")

print ("**** Test 3: Redirect ****")
testHTTP("http://steamcommunity.com", "/id/robe_16/home/", "close")

print ("**** Test 4: Intentional HTTP Fail ****")
testHTTP("https://www.google.co.uk", "/asdfg", "close")

print ("**** Test 5: 'http://' correction ****")
testHTTP("www.google.co.uk", "/search", "close")
