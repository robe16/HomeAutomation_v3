import nest_static_vars
import json
from object_tv_lg import object_LGTV
from object_tivo import object_TIVO


def read_config_devices():
    with open('config_devices.json', 'r') as data_file:
        data = json.load(data_file)
    data_allrooms = data["rooms"]
    #
    x=0
    ARRobjects = []
    while x<len(data_allrooms):
        y=0
        groups=[]
        data_room=data_allrooms[x]
        while y<len(data_room["groups"]):
            z=0
            devices=[]
            data_group=data_room["groups"][y]
            while z<len(data_group["devices"]):
                #
                data_device=data_group["devices"][z]
                if data_device["type"]=="lgtv":
                    devices.append(object_LGTV(data_device["name"].encode('ascii'),
                                               data_device["ipaddress"].encode('ascii'),
                                               8080,
                                               STRpairingkey=data_device["pairingkey"].encode('ascii'),
                                               BOOLtvguide_use=data_device["usetvguide"]))
                elif data_device["type"]=="tivo":
                    devices.append(object_TIVO(data_device["name"].encode('ascii'),
                                               data_device["ipaddress"].encode('ascii'),
                                               31339,
                                               STRaccesskey=data_device["mak"].encode('ascii'),
                                               BOOLtvguide_use=data_device["usetvguide"]))
                #
                z+=1
            groups.append([data_group["name"].encode('ascii'), devices])
            y+=1
        ARRobjects.append([data_room["name"].encode('ascii'), groups])
        x+=1
    return ARRobjects


def read_config_nest():
    with open('config_nest.json', 'r') as data_file:
        data = json.load(data_file)
    ARRnestData = []
    ARRnestData.append(data['nest']['pincode'])
    ARRnestData.append(data['nest']['token'])
    ARRnestData.append(data['nest']['tokenexpiry'])
    return ARRnestData


def write_config_devices(ARRobjects):
    try:
        with open('config_devices.json', 'w') as outfile:
            outfile.write(json.dumps(create_json_devices(ARRobjects), outfile, indent=4, separators=(',', ': ')))
        return True
    except:
        return False


def write_config_nest(ARRnestData):
    try:
        with open('config_nest.json', 'w') as outfile:
            outfile.write(json.dumps(create_json_nest(ARRnestData), outfile, indent=4, separators=(',', ': ')))
        return True
    except:
        return False


def create_json_devices(ARRobjects):
    DICTrooms=[]
    x=0
    while x<len(ARRobjects):
        DICTgroups=[]
        y=0
        while y<len(ARRobjects[x][1]):
            DICTdevices=[]
            z=0
            while z<len(ARRobjects[x][1][y][1]):
                #
                object=ARRobjects[x][1][y][1][z]
                #
                if isinstance(object, object_LGTV):
                    DICTdevices.append({'name': object.getName(),
                                        'type':'lgtv',
                                        'ipaddress':object.getIP(),
                                        'pairingkey':object.getPairingkey(),
                                        'usetvguide':object.getTvguide_use()})
                elif isinstance(object, object_TIVO):
                    DICTdevices.append({'name': object.getName(),
                                        'type':'tivo',
                                        'ipaddress':object.getIP(),
                                        'mak':object.getAccesskey(),
                                        'usetvguide':object.getTvguide_use()})
                #
                z+=1
            DICTgroups.append({"name": ARRobjects[x][1][y][0], "devices": DICTdevices})
            y+=1
        DICTrooms.append({"name": ARRobjects[x][0], "groups": DICTgroups})
        x+=1
    return {'rooms': DICTrooms}


def create_json_nest(ARRnestData):
    return {'nest': {'pincode': ARRnestData[0], 'token': ARRnestData[1], 'tokenexpiry': ARRnestData[2]}}


'''
******** Example JSON ********
{"rooms":
    [
    {"name": "lounge",
    "groups":
        [
        {"name": "TV",
        "devices":
            [
            {
            "name": "LGTV",
            "type": "lgtv",
            "ipaddress": dataholder.STRloungetv_lgtv_ipaddress,
            "pairingkey": dataholder.STRloungetv_lgtv_pairkey
            "usetvguide": true/false
            },
            {
            "name": "TIVO",
            "type": "tivo",
            "ipaddress": dataholder.STRloungetv_tivo_ipaddress,
            "mak": dataholder.STRloungetv_tivo_mak
            "usetvguide": true/false
            }
            ]
        },
        {
        "Music":
            [
            ]
        }
        ]
    }
    ]
}
{"nest":
    {
    "pincode": "xxxxxx",
    "token": "45678-gfsas-2354656u-hgfds-eretry",
    "tokenexpiry", "xx/xx/xxxx xx:xx:xx"
    }
}
'''