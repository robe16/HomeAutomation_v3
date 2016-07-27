from multiprocessing import Process, Manager
from console_messages import print_msg
from port_listener import start_bottle
from config_devices_create import create_device_threads
from config_devices import get_device_json, count_groups, count_devices
import cfg


################################
# Create queues for each device
################################
#
device_queues = []
#
grp_count = count_groups()
grp_num = 0
#
while grp_num < grp_count:
    dvc_count = count_devices(grp_num)
    dvc_num = 0
    device_queues.append([])
    while dvc_num < dvc_count:
        device_queues[grp_num].append([])
        device_queues[grp_num][dvc_num] = Manager().Queue()
        dvc_num += 1
    grp_num += 1

################################
# Queues for responses back to port_listener
################################
q_response_web_device = Manager().Queue()
q_response_comand = Manager().Queue()

################################
# Queue for shared TV listing info
################################
q_listings = Manager().Queue()
################################


def server_start():
    #
    ################################
    # Create response queue dict
    ################################
    queues = {cfg.key_q_response_web_device: q_response_web_device,
              cfg.key_q_response_command: q_response_comand,
              cfg.key_q_tvlistings: q_listings}
    #
    ################################
    # Process for port_listener
    ################################
    port = 1600
    print_msg('Starting process: "bottle" server for port {port}'.format(port=port))
    process_bottle = Process(target=start_bottle, args=(port, device_queues, queues, ))
    process_bottle.start()
    print_msg('Process started: "bottle" server for port {port}'.format(port=port))
    #
    ################################
    # Process for device threads
    ################################
    print_msg('Starting process: Creation of device threads')
    process_devices = Process(target=create_device_threads, args=(device_queues, queues, ))
    process_devices.start()
    print_msg('Process started: Creation of device threads')
    #
    ################################
    # Process to retrieve TV listings.
    # !!!! Not currently in use due to decommision of radiotimes API !!!!
    ################################
    # print_msg('Starting process: Retrieval of TV listings')
    # process_listings = Process(target=tvlistings_process)
    # process_listings.start()
    # print_msg('Process started: Retrieval of TV listings')
    #
    ################################
    # Use .join() to ensure main process with Manager() items remains open
    ################################
    process_bottle.join()
    process_devices.join()
    #process_listings.join()
    #
    ################################


# Start server
server_start()


# def tvlistings_process():
#     time.sleep(2)
#     # 604800 secs = 7 days
#     while True:
#         try:
#             server_queues.q_listings.put(build_channel_array())
#             print_msg('Building of channels and listings completed')
#             time.sleep(604800)
#         except Exception as e:
#             print_error('Creation of TV listings failed - retrying in 10 seconds')
#             # if creation of listings crashes, retry in 10 seconds
#             time.sleep(10)