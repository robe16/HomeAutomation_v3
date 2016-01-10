import json
import os


def read_list_remotes(devicetype, command):
    with open(os.path.join('lists', 'list_remotes.json'), 'r') as data_file:
        data = json.load(data_file)
    return read_json_remotes(data, devicetype, command)


def read_json_remotes(data, devicetype, command):
    #
    for dict_dvc in data['remotes']:
        for k, v in dict_dvc.items():
            if k == devicetype:
                y = 0
                while y < len(v):
                    if v[y]['name'] == command:
                        return v[y]['command']
                    y += 1
    #
    return False