import json
import os


def read_list_devices():
    with open(os.path.join('lists', 'list_device_types.json'), 'r') as data_file:
        data = json.load(data_file)
        data_file.close()
    if not isinstance(data, dict):
        return data
    else:
        return False


def _get_device_details(type):
    data = read_list_devices()
    if data:
        for item in data:
            if item['type'] == type:
                return item
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