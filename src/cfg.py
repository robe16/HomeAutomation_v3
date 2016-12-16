max_group = 5
max_devices = 5

request_timeout = 10

key_q_response_data = 'data'
key_q_response_command = 'command'

key_q_tvlistings = 'tvlistings'

port_server = 1600

# Code below used to determine and return server information (e.g. ip address on network, mac address, etc)

import socket
from uuid import getnode as get_mac

def my_ip():
    return socket.gethostbyname(socket.gethostname())

def my_mac():
    return ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2))