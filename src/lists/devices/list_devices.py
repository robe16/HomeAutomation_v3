import json
import os
from src.console_messages import print_error


def read_list_devices():
    with open(os.path.join('lists', 'list_device_types.json'), 'r') as data_file:
        data = json.load(data_file)
        data_file.close()
    if isinstance(data, dict):
        return data
    else:
        return False


def _get_device_details(type):
    data = read_list_devices()
    try:
        return data[type]
    except:
        return False


def get_device_name(type):
    item = _get_device_details(type)
    if item:
        return item['name']
    return False


def get_device_logo(type):
    item = _get_device_details(type)
    if item:
        return item['logo']
    return False


def get_device_html_command(type):
    item = _get_device_details(type)
    if item:
        return item['html_command']
    return False


def get_device_html_settings(type):
    item = _get_device_details(type)
    if item:
        return item['html_settings']
    return False


def get_device_settings_dict(type):
    item = _get_device_details(type)
    if item:
        return item['settings_dict']
    return False


def get_device_detail(type, key):
    item = _get_device_details(type)
    if item:
        return item[key]
    return False

def set_device_detail(type, key, value):
    #
    data = json.load(open(os.path.join('lists', 'list_device_types.json'), 'r'))
    #
    data[type][key] = value
    try:
        #
        with open(os.path.join('lists', 'list_device_types.json'), 'w+') as output_file:
            output_file.write(json.dumps(data, indent=4, separators=(',', ': ')))
            output_file.close()
        #
        return True
    except Exception as e:
        print_error('Could not update "list_device_types.json" with new value - ' + str(e))
        return False