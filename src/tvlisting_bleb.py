from datetime import datetime, timedelta
import time
from send_cmds import sendHTTP

# TODO
# http://www.bleb.org/tv/data/listings/

def getlisting(value):
    return None
    #
    x = sendHTTP('http://xmltv.radiotimes.com/xmltv/{code}.dat'.format(code=value), 'close',
                 contenttype='text/xml; charset=utf-8')
    return x.read() if bool(x) else None

def nownext(data):
    # Rules for use of bleb is to wait 2 seconds between requests
    time.sleep(2)
    return None