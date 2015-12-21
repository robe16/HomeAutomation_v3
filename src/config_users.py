import json


def read_config_users():
    with open('config_users.json', 'r') as data_file:
        data = json.load(data_file)
    if not isinstance(data, dict):
        data = json.loads(data)
    if len(data["users"]) == 0:
        return None
    else:
        return data


def get_usernames():
    data = read_config_users()
    if data == None:
        return None
    LSTnames = []
    x = 0
    while x < len(data["users"]):
        LSTnames.append(data["users"][x]["name"])
        x += 1
    return LSTnames


def get_usertheme(user):
    data = read_config_users()
    if data == None:
        return None
    else:
        return data["users"][user]["theme"]


def check_user(user):
    data = read_config_users()
    if not data == None:
        x=0
        while x<len(data['users']):
            if data['users'][x]['name']==user:
                return True
            x+=1
    return False


def get_userchannels(user):
    data = read_config_users()
    if data == None:
        return None
    else:
        LSTchan = []
        pref = data["users"][user]["tvlistings"]
        x = 0
        while x < len(pref):
            LSTchan.append(pref[x])
            x+=1
