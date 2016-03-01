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