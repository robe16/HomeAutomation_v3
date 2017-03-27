import ast
from config.bindings.config_bindings import get_cfg_bindings_json
from lists.bindings.list_bindings import get_binding_logo


def compile_setup():
    #
    data = get_cfg_bindings_json()
    #
    for group in data['bindings']['groups']:
        for thing in group['things']:
            del thing['details_private']
            thing['logo'] = get_binding_logo(thing['device_type'])
    #
    try:
        return ast.literal_eval(data)
    except:
        return data