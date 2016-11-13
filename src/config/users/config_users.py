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
            x=0
            while x<len(data['users']):
                if data['users'][x]['name'] == user:
                    channels = json.load(channels)
                    data['users'][x]['tvlistings'] = channels
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
        x=0
        while x<len(data['users']):
            if data['users'][x]['name']==user:
                return True
            x+=1
    return False


def get_usernames():
    data = read_config_users()
    if data != None:
        LSTnames = []
        x = 0
        while x < len(data["users"]):
            LSTnames.append(data["users"][x]["name"])
            x += 1
        return LSTnames
    return None


def get_usertheme(user):
    data = read_config_users()
    if data != None:
        x=0
        while x<len(data['users']):
            if data['users'][x]['name']==user:
                return data['users'][x]['theme']
            x+=1
    return "light"


def get_userchannels(user):
    data = read_config_users()
    if data != None:
        x=0
        while x<len(data['users']):
            if data['users'][x]['name']==user:
                return data['users'][x]['tvlistings']
            x+=1
    return None


def get_userrole(user):
    data = read_config_users()
    if data != None:
        x=0
        while x<len(data['users']):
            if data['users'][x]['name']==user:
                return data['users'][x]['role']
            x+=1
    return None


def get_userimage(user):
    data = read_config_users()
    if data != None:
        x=0
        while x<len(data['users']):
            if data['users'][x]['name']==user:
                if data['users'][x]['image'] != "":
                    return data['users'][x]['image']
            x+=1
    return "default.png"