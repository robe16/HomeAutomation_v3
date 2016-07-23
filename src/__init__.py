from multiprocessing import Process, Queue
from console_messages import print_msg
from port_listener import start_bottle


def server_start():
    port = 1600
    print_msg('Starting process: "bottle" server for port {port}'.format(port=port))
    process_bottle = Process(target=start_bottle, args=(port,))
    process_bottle.start()
    print_msg('Process started: "bottle" server for port {port}'.format(port=port))
    ################################
    # Below is used for the process to retrieve TV listings. Not currently in use due to decommision of radiotimes API
    ################################
    # print_msg('Starting process: Retrieval of TV listings')
    # process_listings = Process(target=tvlistings_process)
    # process_listings.start() #mute/unmute this line if required for testing purposes
    # process_listingsint_msg('Process started: Retrieval of TV listings')
    ################################


# Start server
server_start()


# def tvlistings_process():
#     time.sleep(2)
#     # 604800 secs = 7 days
#     while True:
#         try:
#             q_listings.put(build_channel_array())
#             print_msg('Building of channels and listings completed')
#             time.sleep(604800)
#         except Exception as e:
#             print_error('Creation of TV listings failed - retrying in 10 seconds')
#             # if creation of listings crashes, retry in 10 seconds
#             time.sleep(10)


# def _check_tvlistingsqueue():
#     # Check listings in queue
#     if not q_listings.empty():
#         temp = q_listings.get()
#         q_listings.put(temp)
#         return temp
#     else:
#         return False


# Create process for creating retrieving TV Listings and creating objects in queue
# q_listings = Queue()