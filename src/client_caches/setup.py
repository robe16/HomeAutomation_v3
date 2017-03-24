import ast
from config.bindings.config_bindings import get_cfg_bindings_json
from lists.bindings.list_bindings import get_binding_logo


def compile_setup():
    #
    data = get_cfg_bindings_json()
    #
    for r in data['bindings']['devices']['groups']:
        for d in data['bindings']['devices']['groups'][r]['devices']:
            del data['bindings']['devices']['groups'][r]['devices'][d]['details']
            data['bindings']['devices']['groups'][r]['devices'][d]['logo'] = get_binding_logo(data['bindings']['devices']['groups'][r]['devices'][d]['device_type'])
            #
    #
    try:
        return ast.literal_eval(data)
    except:
        return data