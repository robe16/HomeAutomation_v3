from config_devices import get_device_json
from object_device_tv_lg_netcast import object_tv_lg_netcast
from object_device_tivo import object_tivo
from object_device_other import object_other
from object_device_xbox_one import object_xbox_one
from object_device_raspberrypi import object_raspberrypi
from object_nest_account import object_nest_account


def create_device_object(grp_name, dvc_label):
    #
    data = get_device_json()
    #
    return _create_device_object(data[grp_name]['group'], data[grp_name]['devices'][dvc_label])


def _create_device_object(grp_name, data_device):
    device_type = data_device['device']
    #
    if device_type=="tv_lg_netcast":
        return object_tv_lg_netcast(label = data_device['details']['name'].encode('ascii'),
                                    group = grp_name,
                                    ipaddress = data_device['details']['ipaddress'].encode('ascii'),
                                    port = 8080,
                                    pairingkey = data_device['details']['pairingkey'].encode('ascii'))
    elif device_type=="tivo":
        return object_tivo(label = data_device['details']['name'].encode('ascii'),
                           group = grp_name)
    elif device_type=="xbox_one":
        return object_xbox_one(label = data_device['details']['name'].encode('ascii'),
                               group = grp_name,
                               ipaddress = data_device['details']['ipaddress'].encode('ascii'))
    elif device_type=="raspberrypi":
        return object_raspberrypi(label = data_device['details']['name'].encode('ascii'),
                                  group = grp_name,
                                  ipaddress = data_device['details']['ipaddress'].encode('ascii'))
    elif device_type=="other":
        return object_other(label = data_device['details']['name'].encode('ascii'),
                            group = grp_name,
                            ipaddress = data_device['details']['ipaddress'].encode('ascii'))
    elif device_type=="nest_account":
        return object_nest_account(group = grp_name,
                                   token = data_device['details']['token'].encode('ascii'),
                                   tokenexpiry = data_device['details']['tokenexpiry'].encode('ascii'),
                                   pincode = data_device['details']['pincode'].encode('ascii'),
                                   state = data_device['details']['state'].encode('ascii'))
    else:
        return None