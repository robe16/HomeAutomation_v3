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


def count_groups():
    #
    data = get_device_json()
    #
    return len(data)


def get_group_config_name(grp_num):
    #
    data = get_device_json()
    #
    return data[str(grp_num)]['name']


def count_devices(grp_num):
    #
    data = get_device_json()
    #
    return len(data[str(grp_num)]['devices'])


def get_device_config_type(grp_num, dvc_num):
    #
    data = get_device_json()
    #
    return data[str(grp_num)]['devices'][str(dvc_num)]['device']


def get_device_config_name(grp_num, dvc_num):
    #
    data = get_device_json()
    #
    return data[str(grp_num)]['devices'][str(dvc_num)]['details']['name']


def get_device_config_detail(grp_num, dvc_num, key):
    #
    data = get_device_json()
    #
    return data[str(grp_num)]['devices'][str(dvc_num)]['details'][key]


def set_device_config_detail(grp_num, dvc_num, key, value):
    #
    data = get_device_json()
    #
    data[str(grp_num)]['devices'][str(dvc_num)]['details'][key] = value
    #
    return write_config_devices(data)