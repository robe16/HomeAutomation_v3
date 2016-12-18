import ast
from src.config.bundles.config_bundles import get_cfg_bundles_json
from src.lists.devices.list_devices import get_device_logo


def compile_setup():
    #
    data = get_cfg_bundles_json()
    #
    for a in data['structure']['accounts']:
        del data['structure']['accounts'][a]['details']
        data['structure']['accounts'][a]['logo'] = get_device_logo(data['structure']['accounts'][a]['account_type'])
        #
    for r in data['structure']['rooms']:
        for d in data['structure']['rooms'][r]['devices']:
            del data['structure']['rooms'][r]['devices'][d]['details']
            data['structure']['rooms'][r]['devices'][d]['logo'] = get_device_logo(data['structure']['rooms'][r]['devices'][d]['device_type'])
            #
    #
    try:
        return ast.literal_eval(data)
    except:
        return data