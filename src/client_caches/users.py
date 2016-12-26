import ast
from config.users.config_users import read_config_users


def compile_users():
    #
    data = read_config_users()
    #
    for id in data['users']:
        del data['users'][id]['pin']
    #
    try:
        return ast.literal_eval(data)
    except:
        return data