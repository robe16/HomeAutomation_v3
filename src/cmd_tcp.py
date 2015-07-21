import telnetlib

def sendTCP(ipaddress, data):
    # Send data via tcp to IP address over network conection
    try:
        tn = telnetlib.Telnet(ipaddress)
        tn.write(data + '\n')
        return True
    except Exception:
        return False