import ast
# from config.users.config_users import get_usernames


def compile_tvlistings():
    #
    data = {}
    # data['users'] = get_usernames()
    #
    try:
        return ast.literal_eval(data)
    except:
        return data