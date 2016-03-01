import json
import os
import ast


def write_config_devices(new_data):
    try:
        #
        try:
            new_data = ast.literal_eval(new_data)
        except:
            new_data = new_data
        #
        with open(os.path.join('config', 'config_devices.json'), 'w+') as output_file:
            output_file.write(json.dumps(new_data, indent=4, separators=(',', ': ')))
            output_file.close()
        #
        return True
    except Exception as e:
        return False


def get_device_json():
    with open(os.path.join('config', 'config_devices.json'), 'r') as data_file:
        return json.load(data_file)


# def get_device(grp_name, dvc_label):
#     #
#     data = get_device_json()
#     #
#     return create_device_object(grp_name, data[grp_name]['devices'][dvc_label])


def get_device_config_detail(grp_name, dvc_label, key):
    #
    data = get_device_json()
    #
    return data[grp_name]['devices'][dvc_label]['details'][key]


def set_device_config_detail(grp_name, dvc_label, key, value):
    #
    data = get_device_json()
    #
    data[grp_name]['devices'][dvc_label]['details'][key] = value
    #
    return write_config_devices(data)


# def create_device_object_array():
#     temp_array = []
#     #
#     data = get_device_json()
#     #
#     for data_group in data:
#         temp_devices = []
#         for dvc in data_group['devices']:
#             temp_devices.append(_create_device_object(data_group['group'], dvc))
#         temp_array.append({'name': data_group['group'],
#                            'devices': temp_devices})
#     #
#     return temp_array


# def create_device_object(grp_name, data_device):
#     device_type = data_device['device']
#     #
#     if device_type=="tv_lg_netcast":
#         return object_tv_lg_netcast(label = data_device['details']['name'].encode('ascii'),
#                                     group = grp_name,
#                                     ipaddress = data_device['details']['ipaddress'].encode('ascii'),
#                                     port = 8080,
#                                     pairingkey = data_device['details']['pairingkey'].encode('ascii'))
#     elif device_type=="tivo":
#         return object_tivo(label = data_device['details']['name'].encode('ascii'),
#                            group = grp_name,
#                            ipaddress = data_device['details']['ipaddress'].encode('ascii'),
#                            port = 31339,
#                            accesskey = data_device['details']['mak'].encode('ascii'))
#     elif device_type=="xbox_one":
#         return object_xbox_one(label = data_device['details']['name'].encode('ascii'),
#                                group = grp_name,
#                                ipaddress = data_device['details']['ipaddress'].encode('ascii'))
#     elif device_type=="raspberrypi":
#         return object_raspberrypi(label = data_device['details']['name'].encode('ascii'),
#                                   group = grp_name,
#                                   ipaddress = data_device['details']['ipaddress'].encode('ascii'))
#     elif device_type=="other":
#         return object_other(label = data_device['details']['name'].encode('ascii'),
#                             group = grp_name,
#                             ipaddress = data_device['details']['ipaddress'].encode('ascii'))
#     elif device_type=="nest_account":
#         return object_nest_account(group = grp_name,
#                                    token = data_device['details']['token'].encode('ascii'),
#                                    tokenexpiry = data_device['details']['tokenexpiry'].encode('ascii'),
#                                    pincode = data_device['details']['pincode'].encode('ascii'),
#                                    state = data_device['details']['state'].encode('ascii'))
#     else:
#         return None