from multiprocessing import Process, Manager

import cfg
from port_listener import start_bottle
from config.bundles.config_bundles import get_cfg_bundles_json
from config.bundles.config_bundles import get_cfg_idlist_rooms, get_cfg_idlist_devices, get_cfg_idlist_accounts
from config.bundles.config_bundles_create import create_bundles
from log.console_messages import print_msg
import setup

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
    print("r - Run the server\n" +
          "s - Setup the server\n" +
          "e - Exit\n")
    #
    input_var = raw_input("Type the required option number followed by the return key: ")
    print("\n****************************************************************\n")
    #
    # if input_var==None:
    #     print("\nOperation timed out: default option ('r') selected")
    #     input_var="r"
    # else:
    #     input_var=str(input_var)
    #
    if input_var=='s':
        #
        setup.console_setup()
        #
    elif input_var=='r':
        #
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
        print_msg('HomeControl-server exiting')
        print("\n****************************************************************\n")
        #
    else:
        #
        print_msg("Invalid entry, please try again!!")
        print("\n****************************************************************\n")