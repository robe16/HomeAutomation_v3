from multiprocessing import Process, Manager

import cfg
from port_listener import start_bottle
from config.bundles.config_bundles import get_cfg_bundles_json
from config.bundles.config_bundles import get_cfg_idlist_rooms, get_cfg_idlist_devices, get_cfg_idlist_accounts
from config.bundles.config_bundles_create import create_bundles
from log.console_messages import print_msg


################################
# Startup option
################################
print("\n****************************************************************")
print("********************** HomeControl-server **********************")
print("****************************************************************\n")
#
run = True
#
while run:
    #
    input_var = 'r' #default
    print("r - Run the server\n" +
          "s - Setup the server\n" +
          "e - Exit\n")
    input_var = str(raw_input("Type the required option number followed by the return key: "))
    # TODO: set a timeout on keyboard entry so that defaults to 'r' when auto-runs when Pi is switched on
    #
    if input_var=='s':
        #
        print("\n****************************************************************\n")
        # TODO
        print("\n****************************************************************\n")
        #
    elif input_var=='r':
        #
        print("\n****************************************************************\n")
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
        process_object.join()
        process_bottle.join()
        ################################
        print("\n****************************************************************\n")
        #
    elif input_var=='e':
        #
        run = False
        print("\n****************************************************************\n")
        print_msg('HomeControl-server exitting')
        print("\n****************************************************************\n")
        #
    else:
        #
        print("\n****************************************************************\n")
        print_msg("Invalid entry, please try again!!")
        print("\n****************************************************************\n")