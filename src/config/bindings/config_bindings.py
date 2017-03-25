import json
import os
import ast

################################################################################################
# Master defs to read and write json config file
################################################################################################

def write_config_bindings(new_data):
    try:
        #
        try:
            new_data = ast.literal_eval(new_data)
        except:
            new_data = new_data
        #
        with open(os.path.join(os.path.dirname(__file__), 'config_bindings.json'), 'w+') as output_file:
            output_file.write(json.dumps(new_data, indent=4, separators=(',', ': ')))
            output_file.close()
        #
        return True
    except Exception as e:
        return False


def get_cfg_bindings_json():
    with open(os.path.join(os.path.dirname(__file__), 'config_bindings.json'), 'r') as data_file:
        return json.load(data_file)

################################################################################################
# Return count of groups and devices
################################################################################################


def get_cfg_count_groups():
    #
    data = get_cfg_bindings_json()
    #
    return len(data['bindings']['groups'])


def get_cfg_count_devices(group_id):
    #
    data = get_cfg_bindings_json()
    #
    return len(data['bindings']['groups'][group_id]['devices'])

################################################################################################
# Return list of group and device ids
################################################################################################


def get_cfg_idlist_groups():
    #
    data = get_cfg_bindings_json()
    #
    r_list = []
    #
    for key, value in data['bindings']['groups'].iteritems():
        r_list.append(key)
    #
    return r_list


def get_cfg_idlist_devices(group_id):
    #
    data = get_cfg_bindings_json()
    #
    d_list = []
    #
    for key, value in data['bindings']['groups'][group_id]['devices'].iteritems():
        d_list.append(key)
    #
    return d_list

################################################################################################
# Return number/index for group and device
################################################################################################


def get_cfg_group_index(group_id):
    #
    data = get_cfg_bindings_json()
    count = 0
    #
    for key, value in data['bindings']['groups'].iteritems():
        if key == group_id:
            return count
        count += 1
    #
    return -1


def get_cfg_device_index(group_id, device_id):
    #
    data = get_cfg_bindings_json()
    count = 0
    #
    for key, value in data['bindings']['groups'][group_id]['devices'].iteritems():
        if key == device_id:
            return count
        count += 1
    #
    return -1

################################################################################################
# Return structure properties
################################################################################################


def get_cfg_structure_postcode():
    #
    return get_cfg_structure_value('structure_postcode')

def get_cfg_structure_town():
    #
    return get_cfg_structure_value('structure_town')

################################################################################################
# Return name of group and device
################################################################################################


def get_cfg_group_name(group_id):
    #
    return get_cfg_group_value(group_id, 'group_name')


def get_cfg_device_name(group_id, device_id):
    #
    return get_cfg_device_value(group_id, device_id, 'device_name')

################################################################################################
# Return type of device
################################################################################################


def get_cfg_device_type(group_id, device_id):
    #
    return get_cfg_device_value(group_id, device_id, 'device_type')

################################################################################################
# Return private detail value of device
################################################################################################


def get_cfg_device_detail(group_id, device_id, detail):
    #
    details = get_cfg_device_value(group_id, device_id, 'details')
    #
    return details[detail]

################################################################################################
# Return public detail value of device
################################################################################################


def get_cfg_device_detail_public(group_id, device_id, detail):
    #
    details = get_cfg_device_value(group_id, device_id, 'details_public')
    #
    return details[detail]

################################################################################################
# Save private detail value of device
################################################################################################


def set_cfg_device_detail(group_id, device_id, detail, value):
    #
    data = get_cfg_bindings_json()
    #
    data['bindings']['groups'][group_id]['devices'][device_id]['details'][detail] = value
    #
    return write_config_bindings(data)

################################################################################################
# Return enabled status and other details of info_service
################################################################################################


def get_cfg_info_enabled(info_type):
    #
    enabled = get_cfg_info_value(info_type, 'enabled')
    #
    return enabled


def get_cfg_info_detail(info_type, key):
    #
    enabled = get_cfg_info_value(info_type, key)
    #
    return enabled

################################################################################################
# Save detail value of info_service
################################################################################################


def set_cfg_info_detail(info_type, detail, value):
    #
    data = get_cfg_bindings_json()
    #
    data['info_services'][info_type][detail] = value
    #
    return write_config_bindings(data)

################################################################################################
# Save public detail value of device
################################################################################################


def set_cfg_device_detail_public(group_id, device_id, detail, value):
    #
    data = get_cfg_bindings_json()
    #
    data['bindings']['groups'][group_id]['devices'][device_id]['details_public'][detail] = value
    #
    return write_config_bindings(data)

################################################################################################
# Return value for structure group and device
# (used as 'master' code for returning name, type, etc. in above defs)
################################################################################################


def get_cfg_structure_value(key):
    #
    data = get_cfg_bindings_json()
    #
    return data['structure'][key]


def get_cfg_group_value(group_id, key):
    #
    data = get_cfg_bindings_json()
    #
    return data['bindings']['groups'][group_id][key]


def get_cfg_device_value(group_id, device_id, key):
    #
    data = get_cfg_bindings_json()
    #
    return data['bindings']['groups'][group_id]['devices'][device_id][key]


def get_cfg_info_value(info_type, key):
    #
    data = get_cfg_bindings_json()
    #
    return data['bindings']['info_services'][info_type][key]

################################################################################################
################################################################################################