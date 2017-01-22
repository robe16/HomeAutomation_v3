import ast
from config.bundles.config_bundles import get_cfg_bundles_json
from lists.devices.list_devices import get_device_logo


def compile_setup():
    #
    data = get_cfg_bundles_json()
    #
    for a in data['accounts']:
        del data['accounts'][a]['details']
        data['accounts'][a]['logo'] = get_device_logo(data['accounts'][a]['account_type'])
        #
    for r in data['rooms']:
        for d in data['rooms'][r]['devices']:
            del data['rooms'][r]['devices'][d]['details']
            data['rooms'][r]['devices'][d]['logo'] = get_device_logo(data['rooms'][r]['devices'][d]['device_type'])
            #
    #
    try:
        return ast.literal_eval(data)
    except:
        return data