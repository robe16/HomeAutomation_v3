import threading

from src.bundles.accounts.nest.nest import account_nest
from src.bundles.devices.tivo.tivo import device_tivo
from src.bundles.devices.tv_lg_netcast.tv_lg_netcast import device_tv_lg_netcast
from src.config.devices.config_devices import get_cfg_device_type, get_cfg_account_type
from src.config.devices.config_devices import get_cfg_idlist_rooms, get_cfg_idlist_devices, get_cfg_idlist_accounts
from src.log.console_messages import print_msg


def create_device_threads(q_devices, q_accounts, queues):
    #
    t = 0
    thread = []
    #
    r_list = get_cfg_idlist_rooms()
    r_num = 0
    #
    while r_num < len(r_list):
        d_list = get_cfg_idlist_devices(r_list[r_num])
        d_num = 0
        #
        while d_num < len(d_list):
            #
            thread.append(threading.Thread(target=_create_device, args=(r_list[r_num],
                                                                        d_list[d_num],
                                                                        q_devices[r_num][d_num],
                                                                        queues)))
            thread[t].daemon = True
            thread[t].start()
            #
            print_msg('Thread created: {type}'.format(type=get_cfg_device_type(r_list[r_num], d_list[d_num])),
                      dvc_or_acc_id=r_list[r_num]+':'+d_list[d_num])
            #
            t += 1
            d_num += 1
        r_num += 1
        #
    #
    a_list = get_cfg_idlist_accounts()
    a_num = 0
    #
    while a_num < len(a_list):
        #
        thread.append(threading.Thread(target=_create_account, args=(a_list[a_num],
                                                                     q_accounts[a_num],
                                                                     queues)))
        thread[t].daemon = True
        thread[t].start()
        #
        print_msg('Thread created: {type}'.format(type=get_cfg_account_type(a_list[a_num])),
                  dvc_or_acc_id=a_list[a_num])
        #
        t += 1
        a_num += 1
    #
    x = 0
    while x < t:
        thread[x].join()


def _create_device(room_id, device_id, q_dvc, queues):
    device_type = get_cfg_device_type(room_id, device_id)
    #
    if device_type=="tv_lg_netcast":
        device_tv_lg_netcast(room_id=room_id,
                             device_id=device_id,
                             q_dvc=q_dvc,
                             queues=queues)
    elif device_type=="tivo":
        device_tivo(room_id=room_id,
                    device_id=device_id,
                    q_dvc=q_dvc,
                    queues=queues)


def _create_account(account_id, q_acc, queues):
    device_type = get_cfg_account_type(account_id)
    #
    if device_type=="nest_account":
        account_nest(account_id=account_id,
                     q_acc=q_acc,
                     queues=queues)