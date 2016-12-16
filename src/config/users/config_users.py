import json
import os


def read_config_users():
    with open(os.path.join('config', 'config_users.json'), 'r') as data_file:
        data = json.load(data_file)
        data_file.close()
    if not isinstance(data, dict):
        data = json.loads(data)
    if len(data["users"]) == 0:
        return None
    else:
        return data


def update_user_channels(user, channels):
    try:
        with open(os.path.join('config', 'config_users.json'), 'r') as data_file:
            data = json.load(data_file)
            data_file.close()
        if data != None:
            for id in data['users']:
                if data['users'][id]['name'] == user:
                    channels = json.load(channels)
                    data['users'][id]['tvlistings'] = channels
                    with open(os.path.join('config', 'config_users.json'), 'w+') as output_file:
                        output_file.write(json.dumps(data, indent=4, separators=(',', ': ')))
                        output_file.close()
                    return True
                x+=1
        return False
    except:
        return False


def check_user(user):
    data = read_config_users()
    if data != None:
        for id in data['users']:
            if data['users'][id]['name']==user:
                return True
    return False


def check_pin(user, pin):
    data = read_config_users()
    if data != None:
        for id in data['users']:
            if data['users'][id]['name']==user:
                if data['users'][id]['pin'] == pin:
                    return True
                else:
                    return False
    return False


def get_usernames():
    data = read_config_users()
    if data != None:
        LSTnames = []
        for id in data['users']:
            LSTnames.append(data["users"][id]["name"])
        return LSTnames
    return None


def get_userchannels(user):
    data = read_config_users()
    if data != None:
        for id in data['users']:
            if data['users'][id]['name']==user:
                return data['users'][id]['tvlistings']
    return None


def get_userrole(user):
    data = read_config_users()
    if data != None:
        for id in data['users']:
            if data['users'][id]['name']==user:
                return data['users'][id]['role']
    return None


def get_userimage(user):
    data = read_config_users()
    if data != None:
        for id in data['users']:
            if data['users'][id]['name']==user:
                if data['users'][id]['image'] != "":
                    return data['users'][id]['image']
    return "default.png"