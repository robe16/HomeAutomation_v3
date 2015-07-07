import urllib2
#import urllib.request
#import urllib.parse

def sendHTTP(ipaddress, path, connection, data=False):
    '''Send data via http to IP address over network conection'''
    if not ipaddress.startswith("http"):
        ipaddress = "http://" + ipaddress
    if data:
        data = urllib2.urlencode(data)
        #data = data.encode('utf-8')
        req = urllib2.Request(ipaddress+path, data=data)
    else:
        req = urllib2.Request(ipaddress+path)
    req.add_header("content-type","text/xml; charset=utf-8")
    req.add_header("Connection", connection)
    req.add_header("User-Agent","Linux/2.6.18 UDAP/2.0 CentOS/5.8")
    try:
        return urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        return e
    except urllib2.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        return e


def sendTCP():
    '''Send data via tcp to IP address over network conection'''
    #do something
    return False
