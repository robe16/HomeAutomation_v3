import json
import os
import ast
from object_device_tv_lg_netcast import object_tv_lg_netcast
from object_device_tivo import object_tivo
from object_device_other import object_other
from object_device_xbox_one import object_xbox_one
from object_device_raspberrypi import object_raspberrypi
from object_nest_account import object_nest_account


def write_config_devices(new_data):
    try:
        #
        new_data = ast.literal_eval(new_data)
        #
        with open(os.path.join('config', 'config_devices.json'), 'w+') as output_file:
            output_file.write(json.dumps(new_data, indent=4, separators=(',', ': ')))
            output_file.close()
        #
        return True
    except:
        return False


def get_device_json():
    with open(os.path.join('config', 'config_devices.json'), 'r') as data_file:
        return json.load(data_file)


def create_device_object_array():
    temp_array = []
    #
    data = get_device_json()
    #
    for data_group in data:
        temp_devices = []
        for dvc in data_group['devices']:
            temp_devices.append(_create_device_object(dvc))
        temp_array.append({'name': data_group['group'],
                           'devices': temp_devices})
    #
    return temp_array


def _create_device_object(data_device):
    device_type = data_device['device']
    #
    if device_type=="tv_lg_netcast":
        return object_tv_lg_netcast(label = data_device['details']['name'].encode('ascii'),
                                    ipaddress = data_device['details']['ipaddress'].encode('ascii'),
                                    port = 8080,
                                    pairingkey = data_device['details']['pairingkey'].encode('ascii'))
    elif device_type=="tivo":
        return object_tivo(label = data_device['details']['name'].encode('ascii'),
                           ipaddress = data_device['details']['ipaddress'].encode('ascii'),
                           port = 31339,
                           accesskey = data_device['details']['mak'].encode('ascii'))
    elif device_type=="xbox_one":
        return object_xbox_one(label = data_device['details']['name'].encode('ascii'),
                               ipaddress = data_device['details']['ipaddress'].encode('ascii'))
    elif device_type=="raspberrypi":
        return object_raspberrypi(label = data_device['details']['name'].encode('ascii'),
                                  ipaddress = data_device['details']['ipaddress'].encode('ascii'))
    elif device_type=="other":
        return object_other(label = data_device['details']['name'].encode('ascii'),
                            ipaddress = data_device['details']['ipaddress'].encode('ascii'))
    elif device_type=="nest_account":
        return object_nest_account(token = data_device['details']['token'].encode('ascii'),
                                   tokenexpiry = data_device['details']['tokenexpiry'].encode('ascii'),
                                   pincode = data_device['details']['pincode'].encode('ascii'))
    else:
        return None