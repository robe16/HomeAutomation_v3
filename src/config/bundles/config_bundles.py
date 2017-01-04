import json
import os
import ast

################################################################################################
# Master defs to read and write json config file
################################################################################################

def write_config_bundles(new_data):
    try:
        #
        try:
            new_data = ast.literal_eval(new_data)
        except:
            new_data = new_data
        #
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'config_bundles.json'), 'w+') as output_file:
            output_file.write(json.dumps(new_data, indent=4, separators=(',', ': ')))
            output_file.close()
        #
        return True
    except Exception as e:
        return False


def get_cfg_bundles_json():
    with open(os.path.join(os.path.dirname(__file__), os.pardir, 'config_bundles.json'), 'r') as data_file:
        return json.load(data_file)

################################################################################################
# Return count of rooms, bundles and accounts
################################################################################################


def get_cfg_count_rooms():
    #
    data = get_cfg_bundles_json()
    #
    return len(data['structure']['rooms'])


def get_cfg_count_devices(room_id):
    #
    data = get_cfg_bundles_json()
    #
    return len(data['structure']['rooms'][room_id]['devices'])


def get_cfg_count_accounts():
    #
    data = get_cfg_bundles_json()
    #
    return len(data['structure']['accounts'])

################################################################################################
# Return list of room, device and account ids
################################################################################################


def get_cfg_idlist_rooms():
    #
    data = get_cfg_bundles_json()
    #
    r_list = []
    #
    for key, value in data['structure']['rooms'].iteritems():
        r_list.append(key)
    #
    return r_list


def get_cfg_idlist_devices(room_id):
    #
    data = get_cfg_bundles_json()
    #
    d_list = []
    #
    for key, value in data['structure']['rooms'][room_id]['devices'].iteritems():
        d_list.append(key)
    #
    return d_list


def get_cfg_idlist_accounts():
    #
    data = get_cfg_bundles_json()
    #
    a_list = []
    #
    for key, value in data['structure']['accounts'].iteritems():
        a_list.append(key)
    #
    return a_list

################################################################################################
# Return number/index for room, device and account
################################################################################################


def get_cfg_room_index(room_id):
    #
    data = get_cfg_bundles_json()
    count = 0
    #
    for key, value in data['structure']['rooms'].iteritems():
        if key == room_id:
            return count
        count += 1
    #
    return -1


def get_cfg_device_index(room_id, device_id):
    #
    data = get_cfg_bundles_json()
    count = 0
    #
    for key, value in data['structure']['rooms'][room_id]['devices'].iteritems():
        if key == device_id:
            return count
        count += 1
    #
    return -1


def get_cfg_account_index(account_id):
    #
    data = get_cfg_bundles_json()
    count = 0
    #
    for key, value in data['structure']['accounts'].iteritems():
        if key == account_id:
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
# Return name of room, device and account
################################################################################################


def get_cfg_room_name(room_id):
    #
    return get_cfg_room_value(room_id, 'room_name')


def get_cfg_device_name(room_id, device_id):
    #
    return get_cfg_device_value(room_id, device_id, 'device_name')


def get_cfg_account_name(account_id):
    #
    return get_cfg_account_value(account_id, 'account_name')

################################################################################################
# Return type of device and account
################################################################################################


def get_cfg_device_type(room_id, device_id):
    #
    return get_cfg_device_value(room_id, device_id, 'device_type')


def get_cfg_account_type(account_id):
    #
    return get_cfg_account_value(account_id, 'account_type')

################################################################################################
# Return private detail value of device and account
################################################################################################


def get_cfg_device_detail(room_id, device_id, detail):
    #
    details = get_cfg_device_value(room_id, device_id, 'details')
    #
    return details[detail]


def get_cfg_account_detail(account_id, detail):
    #
    details = get_cfg_account_value(account_id, 'details')
    #
    return details[detail]

################################################################################################
# Return public detail value of device and account
################################################################################################


def get_cfg_device_detail_public(room_id, device_id, detail):
    #
    details = get_cfg_device_value(room_id, device_id, 'details_public')
    #
    return details[detail]


def get_cfg_account_detail_public(account_id, detail):
    #
    details = get_cfg_account_value(account_id, 'details_public')
    #
    return details[detail]

################################################################################################
# Save private detail value of device and account
################################################################################################


def set_cfg_device_detail(room_id, device_id, detail, value):
    #
    data = get_cfg_bundles_json()
    #
    data['structure']['rooms'][room_id]['devices'][device_id]['details'][detail] = value
    #
    return write_config_bundles(data)


def set_cfg_account_detail(account_id, detail, value):
    #
    data = get_cfg_bundles_json()
    #
    data['structure']['accounts'][account_id]['details'][detail] = value
    #
    return write_config_bundles(data)

################################################################################################
# Save public detail value of device and account
################################################################################################


def set_cfg_device_detail_public(room_id, device_id, detail, value):
    #
    data = get_cfg_bundles_json()
    #
    data['structure']['rooms'][room_id]['devices'][device_id]['details_public'][detail] = value
    #
    return write_config_bundles(data)


def set_cfg_device_detail_public(account_id, detail, value):
    #
    data = get_cfg_bundles_json()
    #
    data['structure']['accounts'][account_id]['details_public'][detail] = value
    #
    return write_config_bundles(data)

################################################################################################
# Return value for structure room, device and account
# (used as 'master' code for returning name, type, etc. in above defs)
################################################################################################


def get_cfg_structure_value(key):
    #
    data = get_cfg_bundles_json()
    #
    return data['structure'][key]


def get_cfg_room_value(room_id, key):
    #
    data = get_cfg_bundles_json()
    #
    return data['structure']['rooms'][room_id][key]


def get_cfg_device_value(room_id, device_id, key):
    #
    data = get_cfg_bundles_json()
    #
    return data['structure']['rooms'][room_id]['devices'][device_id][key]


def get_cfg_account_value(account_id, key):
    #
    data = get_cfg_bundles_json()
    #
    return data['structure']['accounts'][account_id][key]

################################################################################################
################################################################################################