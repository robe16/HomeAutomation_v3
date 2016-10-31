import json
import os
import ast

################################################################################################
# Master defs to read and write json config file
################################################################################################

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


def get_cfg_device_json():
    with open(os.path.join('config', 'config_devices.json'), 'r') as data_file:
        return json.load(data_file)

################################################################################################
# Return count of structures, rooms, devices and accounts
################################################################################################

def get_cfg_count_structures():
    #
    data = get_cfg_device_json()
    #
    return len(data['structures'])

def get_cfg_count_rooms(structure_id):
    #
    data = get_cfg_device_json()
    #
    return len(data['structures'][structure_id]['rooms'])

def get_cfg_count_devices(structure_id, room_id):
    #
    data = get_cfg_device_json()
    #
    return len(data['structures'][structure_id]['rooms'][room_id]['devices'])

def get_cfg_count_accounts(structure_id):
    #
    data = get_cfg_device_json()
    #
    return len(data['structures'][structure_id]['accounts'])

################################################################################################
# Return list of structure, room, device and account ids
################################################################################################

def get_cfg_idlist_structures():
    #
    data = get_cfg_device_json()
    #
    s_list = []
    #
    for key, value in data['structures'].iteritems():
        s_list.append(key)
    #
    return s_list

def get_cfg_idlist_rooms(structure_id):
    #
    data = get_cfg_device_json()
    #
    r_list = []
    #
    for key, value in data['structures'][structure_id]['rooms'].iteritems():
        r_list.append(key)
    #
    return r_list

def get_cfg_idlist_devices(structure_id, room_id):
    #
    data = get_cfg_device_json()
    #
    d_list = []
    #
    for key, value in data['structures'][structure_id]['rooms'][room_id]['devices'].iteritems():
        d_list.append(key)
    #
    return d_list

def get_cfg_idlist_accounts(structure_id):
    #
    data = get_cfg_device_json()
    #
    a_list = []
    #
    for key, value in data['structures'][structure_id]['accounts'].iteritems():
        a_list.append(key)
    #
    return a_list

################################################################################################
# Return number/index for structure, room, device and account
################################################################################################

def get_cfg_structure_index(structure_id):
    #
    data = get_cfg_device_json()
    count = 0
    #
    for key, value in data['structures'].iteritems():
        if key == structure_id:
            return count
        count += 1
    #
    return -1

def get_cfg_room_index(structure_id, room_id):
    #
    data = get_cfg_device_json()
    count = 0
    #
    for key, value in data['structures'][structure_id]['rooms'].iteritems():
        if key == room_id:
            return count
        count += 1
    #
    return -1

def get_cfg_device_index(structure_id, room_id, device_id):
    #
    data = get_cfg_device_json()
    count = 0
    #
    for key, value in data['structures'][structure_id]['rooms'][room_id]['devices'].iteritems():
        if key == device_id:
            return count
        count += 1
    #
    return -1

def get_cfg_account_index(structure_id, account_id):
    #
    data = get_cfg_device_json()
    count = 0
    #
    for key, value in data['structures'][structure_id]['accounts'].iteritems():
        if key == account_id:
            return count
        count += 1
    #
    return -1


################################################################################################
# Return name of structure, room, device and account
################################################################################################

def get_cfg_structure_name(structure_id):
    #
    return get_cfg_structure_value(structure_id, 'structure_name')

def get_cfg_room_name(structure_id, room_id):
    #
    return get_cfg_room_value(structure_id, room_id, 'room_name')

def get_cfg_device_name(structure_id, room_id, device_id):
    #
    return get_cfg_device_value(structure_id, room_id, device_id, 'device_name')

def get_cfg_account_name(structure_id, account_id):
    #
    return get_cfg_account_value(structure_id, account_id, 'account_name')

################################################################################################
# Return type of device and account
################################################################################################

def get_cfg_device_type(structure_id, room_id, device_id):
    #
    return get_cfg_device_value(structure_id, room_id, device_id, 'device_type')

def get_cfg_account_type(structure_id, account_id):
    #
    return get_cfg_account_value(structure_id, account_id, 'account_type')

################################################################################################
# Return detail value of device and account
################################################################################################

def get_cfg_device_detail(structure_id, room_id, device_id, detail):
    #
    details = get_cfg_device_value(structure_id, room_id, device_id, 'details')
    #
    return details[detail]

def get_cfg_account_detail(structure_id, account_id, detail):
    #
    details = get_cfg_account_value(structure_id, account_id, 'details')
    #
    return details[detail]

################################################################################################
# Save detail value of device and account
################################################################################################

def set_cfg_device_detail(structure_id, room_id, device_id, detail, value):
    #
    data = get_cfg_device_json()
    #
    data['structures'][structure_id]['rooms'][room_id]['devices'][device_id]['details'][detail] = value
    #
    return write_config_devices(data)

def set_cfg_account_detail(structure_id, account_id, detail, value):
    #
    data = get_cfg_device_json()
    #
    data['structures'][structure_id]['accounts'][account_id]['details'][detail] = value
    #
    return write_config_devices(data)

################################################################################################
# Return value for structure, room and device
# (used as 'master' code for returning name, type, etc. in above defs)
################################################################################################

def get_cfg_structure_value(structure_id, key):
    #
    data = get_cfg_device_json()
    #
    return data['structures'][structure_id][key]

def get_cfg_room_value(structure_id, room_id, key):
    #
    data = get_cfg_device_json()
    #
    return data['structures'][structure_id]['rooms'][room_id][key]

def get_cfg_device_value(structure_id, room_id, device_id, key):
    #
    data = get_cfg_device_json()
    #
    return data['structures'][structure_id]['rooms'][room_id]['devices'][device_id][key]

def get_cfg_account_value(structure_id, account_id, key):
    #
    data = get_cfg_device_json()
    #
    return data['structures'][structure_id]['accounts'][account_id][key]

################################################################################################
################################################################################################