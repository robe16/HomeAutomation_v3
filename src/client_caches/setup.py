import ast
from config.bundles.config_bundles import get_cfg_bundles_json
from lists.devices.list_devices import get_device_logo


def compile_setup():
    #
    data = get_cfg_bundles_json()
    #
    for r in data['groups']:
        for d in data['groups'][r]['devices']:
            del data['groups'][r]['devices'][d]['details']
            data['groups'][r]['devices'][d]['logo'] = get_device_logo(data['groups'][r]['devices'][d]['device_type'])
            #
    #
    try:
        return ast.literal_eval(data)
    except:
        return data