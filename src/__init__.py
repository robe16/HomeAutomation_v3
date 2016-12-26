from multiprocessing import Process, Manager

import cfg
from port_listener import start_bottle
from config.bundles.config_bundles import get_cfg_bundles_json
from config.bundles.config_bundles import get_cfg_idlist_rooms, get_cfg_idlist_devices, get_cfg_idlist_accounts
from config.bundles.config_bundles_create import create_bundles
from log.console_messages import print_msg

################################
# Process for object creation
################################
_devices = Manager().dict()
_accounts = Manager().dict()
_infoservices = Manager().dict()
#
print_msg('Starting process: Device, account and infoservice object creation')
process_object = Process(target=create_bundles, args=(_devices, _accounts, _infoservices, ))
process_object.start()
print_msg('Process started: Device, account and infoservice object creation')
#
################################
# Process for port_listener
################################
print_msg('Starting process: "bottle" server for port {port}'.format(port=cfg.port_server))
process_bottle = Process(target=start_bottle, args=(_devices, _accounts, _infoservices, ))
process_bottle.start()
print_msg('Process started: "bottle" server for port {port}'.format(port=cfg.port_server))
#
################################
while True:
    pass
################################