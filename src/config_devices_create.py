from config_devices import count_groups, count_devices, get_device_config_type
from console_messages import print_msg

from object_device_tv_lg_netcast import object_tv_lg_netcast
from object_device_tivo import object_tivo
from object_account_nest import object_nest_account

import threading


def create_device_threads(q_devices, queues):
    #
    grp_count = count_groups()
    grp_num = 0
    t = 0
    thread = []
    #
    while grp_num < grp_count:
        dvc_count = count_devices(grp_num)
        dvc_num = 0
        while dvc_num < dvc_count:
            #
            thread.append(threading.Thread(target=_create_device, args=(grp_num,
                                                                        dvc_num,
                                                                        q_devices[grp_num][dvc_num],
                                                                        queues, )))
            thread[t].daemon = True
            thread[t].start()
            #
            # _create_device(grp_num, dvc_num, q_devices[grp_num][dvc_num], queues)
            #
            print_msg('Thread created - Group {grp_num} Device {dvc_num}: {type}'.format(grp_num=grp_num,
                                                                                         dvc_num=dvc_num,
                                                                                         type=get_device_config_type(grp_num, dvc_num)))
            #
            t += 1
            dvc_num += 1
        grp_num += 1
    #
    x = 0
    while x < t:
        thread[x].join()


def _create_device(grp_num, dvc_num, q_dvc, queues):
    device_type = get_device_config_type(grp_num, dvc_num)
    #
    if device_type=="tv_lg_netcast":
        object_tv_lg_netcast(grp_num=grp_num,
                             dvc_num=dvc_num,
                             q_dvc=q_dvc,
                             queues=queues)
    elif device_type=="tivo":
        object_tivo(grp_num=grp_num,
                             dvc_num=dvc_num,
                             q_dvc=q_dvc,
                             queues=queues)
    elif device_type=="nest_account":
        object_nest_account(grp_num=grp_num,
                            dvc_num=dvc_num,
                            q_dvc=q_dvc,
                            queues=queues)