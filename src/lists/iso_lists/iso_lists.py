import json
import os


def read_list_iso(isoList):
    with open(os.path.join(os.path.dirname(__file__), 'iso_{type}.json'.format(type=isoList)), 'r') as data_file:
        data = json.load(data_file)
        data_file.close()
    if isinstance(data, dict):
        return data
    else:
        return False


def check_exists_language(key):
    data = read_list_iso('language')
    if key not in data:
        raise ValueError("No target in given data")


def check_exists_country(key):
    data = read_list_iso('country')
    if key not in data:
        raise ValueError("No target in given data")


def get_name_from_language(key):
    data = read_list_iso('language')
    try:
        return data[key]['name']
    except Exception as e:
        print('ERROR - ' + str(e))
    return False


def get_name_from_country(key):
    data = read_list_iso('country')
    try:
        return data[key]['name']
    except Exception as e:
        print('ERROR - ' + str(e))
    return False