import ast
from config.bundles.config_bundles import get_cfg_bundles_json
from lists.bundles.list_bundles import get_bundle_logo


def compile_setup():
    #
    data = get_cfg_bundles_json()
    #
    for r in data['bundles']['devices']['groups']:
        for d in data['bundles']['devices']['groups'][r]['devices']:
            del data['bundles']['devices']['groups'][r]['devices'][d]['details']
            data['bundles']['devices']['groups'][r]['devices'][d]['logo'] = get_bundle_logo(data['bundles']['devices']['groups'][r]['devices'][d]['device_type'])
            #
    #
    try:
        return ast.literal_eval(data)
    except:
        return data