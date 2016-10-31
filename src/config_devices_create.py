from config_devices import get_cfg_idlist_structures, get_cfg_idlist_rooms, get_cfg_idlist_devices, get_cfg_idlist_accounts
from config_devices import get_cfg_device_type, get_cfg_account_type
from console_messages import print_msg

from object_device_tv_lg_netcast import object_tv_lg_netcast
from object_device_tivo import object_tivo
from object_account_nest import object_nest_account

import threading


def create_device_threads(q_devices, q_accounts, queues):
    #
    s_list = get_cfg_idlist_structures()
    s_num = 0
    t = 0
    thread = []
    #
    while s_num < len(s_list):
        r_list = get_cfg_idlist_rooms(s_list[s_num])
        r_num = 0
        #
        while r_num < len(r_list):
            d_list = get_cfg_idlist_devices(s_list[s_num], r_list[r_num])
            d_num = 0
            #
            while d_num < len(d_list):
                #
                thread.append(threading.Thread(target=_create_device, args=(s_list[s_num],
                                                                            r_list[r_num],
                                                                            d_list[d_num],
                                                                            q_devices[s_num][r_num][d_num],
                                                                            queues)))
                thread[t].daemon = True
                thread[t].start()
                #
                print_msg('Thread created - Structure "{structure_id}" Room "{room_id}" Device "{device_id}": {type}'.format(structure_id=s_list[s_num],
                                                                                                                             room_id=r_list[r_num],
                                                                                                                             device_id=d_list[d_num],
                                                                                                                             type=get_cfg_device_type(s_list[s_num], r_list[r_num], d_list[d_num])))
                #
                t += 1
                d_num += 1
            r_num += 1
            #
        #
        a_list = get_cfg_idlist_accounts(s_list[s_num])
        a_num = 0
        #
        while a_num < len(a_list):
            #
            thread.append(threading.Thread(target=_create_account, args=(s_list[s_num],
                                                                         a_list[a_num],
                                                                         q_accounts[s_num][a_num],
                                                                         queues)))
            thread[t].daemon = True
            thread[t].start()
            #
            print_msg('Thread created - Structure "{structure_id}" Account "{account_id}": {type}'.format(structure_id=s_list[s_num],
                                                                                                          account_id=a_list[a_num],
                                                                                                          type=get_cfg_account_type(s_list[s_num], a_list[a_num])))
            #
            t += 1
            a_num += 1
            #
        s_num += 1
    #
    x = 0
    while x < t:
        thread[x].join()


def _create_device(structure_id, room_id, device_id, q_dvc, queues):
    device_type = get_cfg_device_type(structure_id, room_id, device_id)
    #
    if device_type=="tv_lg_netcast":
        object_tv_lg_netcast(structure_id=structure_id,
                             room_id=room_id,
                             device_id=device_id,
                             q_dvc=q_dvc,
                             queues=queues)
    elif device_type=="tivo":
        object_tivo(structure_id=structure_id,
                    room_id=room_id,
                    device_id=device_id,
                    q_dvc=q_dvc,
                    queues=queues)


def _create_account(structure_id, account_id, q_dvc, queues):
    device_type = get_cfg_account_type(structure_id, account_id)
    #
    if device_type=="nest_account":
        object_nest_account(structure_id=structure_id,
                            account_id=account_id,
                            q_dvc=q_dvc,
                            queues=queues)