from urllib2 import Request, urlopen, HTTPError
import telnetlib
import time
from console_messages import print_error, print_http
from list_devices import set_device_detail

def sendHTTP(url1, connection, url2='', method=False, data=False, contenttype=False, header_auth=False, retry=0, redirect_type=False):
    #
    # url1              first part of url (if redirected, this is replaced by the new url)
    # connection        type of connection (close, keep-alive, etc)
    # url2              second part of url (if redirected, this is added to the new url)
    # contenttype       used to add 'content-type' header if provided
    # header_auth       used to add 'Authorization' header of provided
    # redirect          counter to limit number of redirects and recursion of def
    # redirect_type     details of device type required to store redirect url into list_devices.json for future use
    #
    if retry >= 5:
        return False
    #
    url = _check_prefix(url1) + url2
    #
    if data:
        req = Request(url, data=data)
    else:
        req = Request(url)
    #
    if bool(method):
        req.get_method = lambda: method
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
        print_http(x.getcode(), 'HTTP request - ' + url)
        return False if not str(x.getcode()).startswith("2") else x
    except HTTPError as h:
        if str(h.getcode()).startswith("3"):
            print_http(h.getcode(), 'Redirect of http request - ' + url + ' - ' + str(h))
            url_redirect = h.headers['Location']
            if redirect_type:
                if url_redirect[-len(url2):]==url2:
                    url_redirect = url_redirect[:(len(url_redirect)-len(url2))]
                set_device_detail(redirect_type, 'redirect_url', url_redirect)
            return sendHTTP(url_redirect, connection, url2=url2, method=method, data=data, contenttype=contenttype, header_auth=header_auth, retry=retry+1)
        else:
            print_http(h.getcode(), 'Could not send http request - ' + url + ' - ' + str(h))
        return False
    except Exception as e:
        print_error('Could not send http request - ' + url + ' - ' + str(e))
        return False


def _check_prefix(url):
    if not url.startswith("http"):
        return "http://" + url
    else:
        return url


def sendTELNET(ipaddress, port, data=None, response=False):
    try:
        tn = telnetlib.Telnet(ipaddress, port)
        time.sleep(0.1)
        output = tn.read_eager() if response else None
        if data:
            tn.write(str(data)+"\n")
            time.sleep(0.1)
            op = tn.read_eager()
            if op=='':
                output = True
            else:
                output = op if (response and not bool(op)) else True
        tn.close()
        return output
    except:
        return False