import json
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


def write_config_devices(ARRobjects):
    try:
        with open('config_devices.json', 'w') as outfile:
            outfile.write(json.dumps(create_json_devices(ARRobjects), outfile, indent=4, separators=(',', ': ')))
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
                if isinstance(object, object_tv_lg_netcast):
                    DICTdevices.append({'name': object.getName(),
                                        'type':'lgtv',
                                        'ipaddress':object.getIP(),
                                        'pairingkey':object.getPairingkey(),
                                        'usetvguide':object.getTvguide_use()})
                elif isinstance(object, object_tivo):
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


def create_device_object_array():
    temp_array = []
    #
    with open('config_devices.json', 'r') as data_file:
        data = json.load(data_file)
    #
    for data_group in data:
        temp_array.append({'name': data_group['group'],
                           'tvguide': data_group['tvguide'],
                           'devices': _create_device_object(data_group)})
    #
    return temp_array


def _create_device_object(data_device):
    device_type = data_device['device']
    try:
        device_source = data_device['details']['source'].encode('ascii')
    except:
        device_source = None
    #
    if device_type=="tv_lg_netcast":
        temp_device = object_tv_lg_netcast(STRname = data_device['details']['name'].encode('ascii'),
                                           STRipaddress = data_device['details']['ipaddress'].encode('ascii'),
                                           INTport = 8080,
                                           STRpairingkey = data_device['details']['pairingkey'].encode('ascii'),
                                           STRsource = device_source)
    elif device_type=="tivo":
        temp_device = object_tivo(STRname = data_device['details']['name'].encode('ascii'),
                                  STRipaddress = data_device['details']['ipaddress'].encode('ascii'),
                                  INTport = 31339,
                                  STRaccesskey = data_device['details']['mak'].encode('ascii'),
                                  STRsource = device_source)
    elif device_type=="xbox_one":
        temp_device = object_xbox_one(STRname = data_device['details']['name'].encode('ascii'),
                                      STRsource = device_source)
    elif device_type=="raspberrypi":
        temp_device = object_raspberrypi(STRname = data_device['details']['name'].encode('ascii'),
                                         STRsource = device_source)
    elif device_type=="other":
        temp_device = object_other(STRname = data_device['details']['name'].encode('ascii'),
                                   STRsource = device_source)
    else:
        temp_device = None
    #
    temp_inputs = []
    try:
        for device in data_device['inputs']:
            temp_inputs.append(_create_device_object(device))
    except:
        temp_inputs = None
    #
    temp_outputs = []
    try:
        for device in data_device['outputs']:
            temp_outputs.append(_create_device_object(device))
    except:
        temp_outputs = None
    #
    if temp_inputs is not None and temp_outputs is not None:
        return {'device': temp_device, 'inputs': temp_inputs, 'outputs': temp_outputs}
    return {'device': temp_device}