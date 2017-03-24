from multiprocessing import Process, Manager

import cfg
from port_listener import start_bottle
from config.bindings.config_bindings import get_cfg_bindings_json
from config.bindings.config_bindings import get_cfg_idlist_groups, get_cfg_idlist_devices
from config.bindings.config_bindings_create import create_bindings
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
input_var = "r"
#
while run:
    #
    if input_var == 's':
        #
        setup.console_setup()
        #
    elif input_var == 'r':
        #
        ################################
        # Process for object creation
        ################################
        _devices = Manager().dict()
        _infoservices = Manager().dict()
        #
        print_msg('Starting process: Device, account and infoservice object creation')
        process_object = Process(target=create_bindings, args=(_devices, _infoservices, ))
        process_object.start()
        print_msg('Process started: Device, account and infoservice object creation')
        #
        ################################
        # Process for port_listener
        ################################
        print_msg('Starting process: "bottle" server for port {port}'.format(port=cfg.port_server))
        process_bottle = Process(target=start_bottle, args=(_devices, _infoservices, ))
        process_bottle.start()
        print_msg('Process started: "bottle" server for port {port}'.format(port=cfg.port_server))
        #
        ################################
        process_object.join()
        process_bottle.join()
        ################################
        print("\n****************************************************************\n")
        #
    elif input_var == 'e':
        #
        run = False
        print_msg('HomeControl-server exiting')
        print("\n****************************************************************\n")
        #
    else:
        #
        print_msg("Invalid entry, please try again!!")
        print("\n****************************************************************\n")
    #
    #
    print("r - Run the server\n" +
          "s - Setup the server\n" +
          "e - Exit\n")
    #
    input_var = raw_input("Type the required option number followed by the return key: ")
    print("\n****************************************************************\n")