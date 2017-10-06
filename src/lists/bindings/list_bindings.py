import json
import os

from log.log import log_error


def read_list_bindings():
    with open(os.path.join(os.path.dirname(__file__), 'list_bindings.json'), 'r') as data_file:
        data = json.load(data_file)
        data_file.close()
    if isinstance(data, dict):
        return data
    else:
        return False


def _get_binding_details(type):
    data = read_list_bindings()
    try:
        return data[type]
    except:
        return False


def get_binding_name(type):
    item = _get_binding_details(type)
    if item:
        return item['name']
    return False


def get_binding_logo(type):
    item = _get_binding_details(type)
    if item:
        return item['logo']
    return False


def get_binding_html_command(type):
    item = _get_binding_details(type)
    if item:
        return item['html_command']
    return False


def get_binding_html_settings(type):
    item = _get_binding_details(type)
    if item:
        return item['html_settings']
    return False


def get_binding_detail(type, key):
    item = _get_binding_details(type)
    if item:
        return item[key]
    return False


def set_binding_detail(type, key, value):
    #
    data = json.load(open(os.path.join(os.path.dirname(__file__), 'list_bindings.json'), 'r'))
    #
    data[type][key] = value
    try:
        #
        with open(os.path.join(os.path.dirname(__file__), 'list_bindings.json'), 'w+') as output_file:
            output_file.write(json.dumps(data, indent=4, separators=(',', ': ')))
            output_file.close()
        #
        return True
    except Exception as e:
        log_error('Could not update "list_bindings.json" with new value - ' + str(e))
        return False