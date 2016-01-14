import json
import os
from object_tv_lg_netcast import object_tv_lg_netcast
from object_tivo import object_tivo
from object_other import object_other
from object_xbox_one import object_xbox_one
from object_raspberrypi import object_raspberrypi


# def read_config_devices():
#     with open('config_devices.json', 'r') as data_file:
#         data = json.load(data_file)
#     return read_json_devices(data)
#
#
# def read_json_devices(dataX):
#     if not isinstance(dataX, dict):
#         data = json.loads(dataX)
#     else:
#         data = dataX
#     data_allrooms = data["rooms"]
#     #
#     x=0
#     ARRobjects = []
#     while x<len(data_allrooms):
#         y=0
#         groups=[]
#         data_room=data_allrooms[x]
#         while y<len(data_room["groups"]):
#             z=0
#             devices=[]
#             data_group=data_room["groups"][y]
#             while z<len(data_group["devices"]):
#                 #
#                 data_device=data_group["devices"][z]
#                 if data_device["type"]=="lgtv":
#                     devices.append(object_tv_lg_netcast(data_device["name"].encode('ascii'),
#                                                data_device["ipaddress"].encode('ascii'),
#                                                8080,
#                                                STRpairingkey=data_device["pairingkey"].encode('ascii'),
#                                                BOOLtvguide_use=data_device["usetvguide"]))
#                 elif data_device["type"]=="tivo":
#                     devices.append(object_tivo(data_device["name"].encode('ascii'),
#                                                data_device["ipaddress"].encode('ascii'),
#                                                31339,
#                                                STRaccesskey=data_device["mak"].encode('ascii'),
#                                                BOOLtvguide_use=data_device["usetvguide"]))
#                 #
#                 z+=1
#             groups.append([data_group["name"].encode('ascii'), devices])
#             y+=1
#         ARRobjects.append([data_room["name"].encode('ascii'), groups])
#         x+=1
#     return ARRobjects


def write_config_devices(data):
    try:
        with open(os.path.join('config', 'config_devices.json'), 'w') as outfile:
            outfile.write(json.dumps(data, outfile, indent=4, separators=(',', ': ')))
        #TODO recreate object array and pass back to __init__ as new config file will overwrite current configuration
        return True
    except:
        return False


'''
******** Example JSON ********
{"nest":
    {
    "pincode": "xxxxxx",
    "token": "45678-gfsas-2354656u-hgfds-eretry",
    "tokenexpiry", "xx/xx/xxxx xx:xx:xx"
    }
}
'''

def get_device_json():
    with open(os.path.join('config', 'config_devices.json'), 'r') as data_file:
        return json.load(data_file)


def create_device_object_array():
    temp_array = []
    #
    data = get_device_json()
    #
    for data_group in data:
        temp_devices = []
        for dvc in data_group['devices']:
            temp_devices.append(_create_device_object(dvc))
        temp_array.append({'name': data_group['group'],
                           'devices': temp_devices})
    #
    return temp_array


def _create_device_object(data_device):
    device_type = data_device['device']
    #
    if device_type=="tv_lg_netcast":
        return object_tv_lg_netcast(STRname = data_device['details']['name'].encode('ascii'),
                                    STRipaddress = data_device['details']['ipaddress'].encode('ascii'),
                                    INTport = 8080,
                                    STRpairingkey = data_device['details']['pairingkey'].encode('ascii'))
    elif device_type=="tivo":
        return object_tivo(STRname = data_device['details']['name'].encode('ascii'),
                           STRipaddress = data_device['details']['ipaddress'].encode('ascii'),
                           INTport = 31339,
                           STRaccesskey = data_device['details']['mak'].encode('ascii'))
    elif device_type=="xbox_one":
        return object_xbox_one(STRname = data_device['details']['name'].encode('ascii'),
                               STRipaddress = data_device['details']['ipaddress'].encode('ascii'))
    elif device_type=="raspberrypi":
        return object_raspberrypi(STRname = data_device['details']['name'].encode('ascii'),
                                  STRipaddress = data_device['details']['ipaddress'].encode('ascii'))
    elif device_type=="other":
        return object_other(STRname = data_device['details']['name'].encode('ascii'),
                            STRipaddress = data_device['details']['ipaddress'].encode('ascii'))
    else:
        return None