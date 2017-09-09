developer_email = 'robe16@hotmail.co.uk'
app_name = 'robe16_HomeControl'

date_format = '%d/%m/%Y %H:%M:%S'

# Code below used to determine and return server information (e.g. ip address on network, mac address, etc)

import socket
from uuid import getnode as get_mac

def my_ip():
    return socket.gethostbyname(socket.gethostname())

def my_mac():
    return ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2))
