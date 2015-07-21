import telnetlib

def sendTCP(ipaddress, port, data):
    # Send data via tcp to IP address over network conection
    try:
        tn = telnetlib.Telnet(host=ipaddress,port=port)
        tn.write(data + '\n')
        tn.close()
        return True
    except Exception as e:
        print "Error when sending telnet command to '%s' - %s" % (ipaddress, e)
        return False