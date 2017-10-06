from multiprocessing import Process, Manager
import sys
from port_listener import start_bottle
from config.bindings.config_bindings_create import create_bindings
from log.log import log_general

################################
# Receive sys arguments
################################
# First argument passed through is the
# port the application listens on
try:
    self_port = sys.argv[1]
except:
    self_port = 1600  # default port
#
################################
# Process for object creation
################################
_things = Manager().dict()
_infoservices = Manager().dict()
#
log_general('Starting process: Device, account and infoservice object creation')
process_object = Process(target=create_bindings, args=(_things, _infoservices, ))
process_object.start()
log_general('Process started: Device, account and infoservice object creation')
#
################################
# Process for port_listener
################################
log_general('Starting process: "bottle" server for port {port}'.format(port=self_port))
process_bottle = Process(target=start_bottle, args=(_things, _infoservices, self_port, ))
process_bottle.start()
log_general('Process started: "bottle" server for port {port}'.format(port=self_port))
#
################################
process_object.join()
process_bottle.join()
################################
print("\n****************************************************************\n")
#
log_general('HomeControl-server exiting')
print("\n****************************************************************\n")