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


def get_cfg_count_things(group_seq):
    #
    data = get_cfg_bindings_json()
    #
    for group in data['bindings']['groups']:
        if group['sequence'] == group_seq:
            return len(group['things'])
    #
    return False


def get_cfg_count_info():
    #
    data = get_cfg_bindings_json()
    #
    return len(data['bindings']['info_services'])



# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# STRUCTURE
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


################################################################################################
# Return structure properties
################################################################################################


def get_cfg_structure_postcode():
    #
    return get_cfg_structure_value('structure_postcode')

def get_cfg_structure_town():
    #
    return get_cfg_structure_value('structure_town')


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# THINGS
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


################################################################################################
# Return sequence for group and Thing from name
################################################################################################


def get_cfg_group_seq(group_name):
    #
    data = get_cfg_bindings_json()
    #
    for group in data['bindings']['groups']:
        if group['name'] == group_name:
            return group['sequence']
    #
    raise Exception


def get_cfg_thing_seq(group_name, thing_name):
    #
    data = get_cfg_bindings_json()
    #
    for group in data['bindings']['groups']:
        if group['name'] == group_name:
            for thing in group['things']:
                if thing['name'] == thing_name:
                    return thing['sequence']
    #
    raise Exception


################################################################################################
# Return name of group and Thing
################################################################################################


def get_cfg_group_name(group_seq):
    return get_cfg_group_value(group_seq, 'name')


def get_cfg_thing_name(group_seq, thing_seq):
    return get_cfg_thing_value(group_seq, thing_seq, 'name')

################################################################################################
# Return type of Thing
################################################################################################

def get_cfg_thing_type(group_seq, thing_seq):
    return get_cfg_thing_value(group_seq, thing_seq, 'type')

################################################################################################
# Return private/public detail value of Thing
################################################################################################


def get_cfg_thing_detail_private(group_seq, thing_seq, detail):
    return get_cfg_thing_detail(group_seq, thing_seq, 'details_private', detail)


def get_cfg_thing_detail_public(group_seq, thing_seq, detail):
    return get_cfg_thing_detail(group_seq, thing_seq, 'details_public', detail)


def get_cfg_thing_detail(group_seq, thing_seq, privpub, detail):
    #
    details = get_cfg_thing_value(group_seq, thing_seq, privpub)
    #
    return details[detail]

################################################################################################
# Save private/public detail value of Thing
################################################################################################


def set_cfg_thing_detail_private(group_seq, thing_seq, detail, value):
    return set_cfg_thing_detail(group_seq, thing_seq, 'details_private', detail, value)


def set_cfg_thing_detail_public(group_seq, thing_seq, detail, value):
    return set_cfg_thing_detail(group_seq, thing_seq, 'details_public', detail, value)


def set_cfg_thing_detail(group_seq, thing_seq, privpub, detail, value):
    #
    data = get_cfg_bindings_json()
    #
    for group in data['bindings']['groups']:
        if group['sequence'] == group_seq:
            #
            for thing in group['things']:
                if thing['sequence'] == thing_seq:
                    #
                    thing[privpub][detail] = value
                    return write_config_bindings(data)
    #
    raise Exception('Requested thing not found in config file')


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# INFO_SERVICE
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


################################################################################################
# Return sequence for info_service from name
################################################################################################


def get_cfg_info_seq(info_name):
    #
    data = get_cfg_bindings_json()
    #
    for info in data['bindings']['info_services']:
        if info['name'] == info_name:
            return info['sequence']
    #
    raise Exception


################################################################################################
# Return name and type of info_service
################################################################################################


def get_cfg_info_name(info_seq):
    return get_cfg_info_value(info_seq, 'name')

def get_cfg_info_type(info_seq):
    return get_cfg_info_value(info_seq, 'type')

################################################################################################
# Return private/public detail info_service of info_service
################################################################################################


def get_cfg_info_detail_private(info_seq, detail):
    return get_cfg_info_detail(info_seq, 'details_private', detail)


def get_cfg_info_detail_public(info_seq, detail):
    return get_cfg_info_detail(info_seq, 'details_public', detail)


def get_cfg_info_detail(info_seq, privpub, detail):
    #
    details = get_cfg_info_value(info_seq, privpub)
    #
    return details[detail]

################################################################################################
# Save private/public detail value of info_service
################################################################################################


def set_cfg_info_detail_private(info_seq, detail, value):
    return set_cfg_info_detail(info_seq, 'details_private', detail, value)


def set_cfg_info_detail_public(info_seq, detail, value):
    return set_cfg_info_detail(info_seq, 'details_public', detail, value)


def set_cfg_info_detail(info_seq, privpub, detail, value):
    #
    data = get_cfg_bindings_json()
    #
    for info in data['bindings']['info_services']:
        if info['sequence'] == info_seq:
            #
            info[privpub][detail] = value
            return write_config_bindings(data)
    #
    raise Exception('Requested thing not found in config file')


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


################################################################################################
# Return value for structure, group, Thing and info_service
# (used as 'master' code for returning name, type, details etc. in above defs)
################################################################################################


def get_cfg_structure_value(key):
    #
    data = get_cfg_bindings_json()
    #
    return data['structure'][key]


def get_cfg_group_value(group_seq, key):
    #
    data = get_cfg_bindings_json()
    #
    for group in data['bindings']['groups']:
        if group['sequence'] == group_seq:
            return group[key]
    #
    raise Exception('Requested group not found in config file')


def get_cfg_thing_value(group_seq, thing_seq, key):
    #
    data = get_cfg_bindings_json()
    #
    for group in data['bindings']['groups']:
        if group['sequence'] == group_seq:
            for thing in group['things']:
                if thing['sequence'] == thing_seq:
                    return thing[key]
    #
    raise Exception('Requested thing not found in config file')


def get_cfg_info_value(info_seq, key):
    #
    data = get_cfg_bindings_json()
    #
    for info in data['bindings']['info_services']:
        if info['sequence'] == info_seq:
            return info[key]
    #
    raise Exception('Requested info_service not found in config file')

################################################################################################
################################################################################################