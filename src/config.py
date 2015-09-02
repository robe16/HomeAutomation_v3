from ConfigParser import ConfigParser
import dataholder
import os
import json
from object_tv_lg import object_LGTV
from object_tivo import object_TIVO


def read_config():
    cfg = ConfigParser()
    if not cfg.read(os.path.join(os.path.dirname(__file__), "config.ini")):
        print 'Error: cannot load config.ini'
        return
    #
    dataholder.STRloungetv_lgtv_ipaddress = cfg.get('Lounge', 'LGTV_ipaddress')
    dataholder.STRloungetv_lgtv_pairkey = cfg.get('Lounge', 'LGTV_pairkey')
    dataholder.STRloungetv_tivo_ipaddress = cfg.get('Lounge', 'TIVO_ipaddress')
    dataholder.STRloungetv_tivo_mak = cfg.get('Lounge', 'TIVO_mak')
    dataholder.STRrocki_ipaddress = cfg.get('Kitchen', 'Rocki_ipaddress')
    dataholder.STRnest_pincode = cfg.get('Nest', 'Pincode')
    dataholder.STRnest_token = cfg.get('Nest', 'Token')
    dataholder.STRnest_tokenexp = cfg.get('Nest', 'Token_expiry')


def write_config():
    #
    cfg = ConfigParser()
    cfgfile = open("config.ini",'w')
    #
    cfg.add_section('Lounge')
    cfg.set('Lounge','LGTV_ipaddress',dataholder.STRloungetv_lgtv_ipaddress)
    cfg.set('Lounge','LGTV_pairkey', dataholder.STRloungetv_lgtv_pairkey)
    cfg.set('Lounge','TIVO_ipaddress', dataholder.STRloungetv_tivo_ipaddress)
    cfg.set('Lounge','TIVO_mak', dataholder.STRloungetv_tivo_mak)
    cfg.add_section('Kitchen')
    cfg.set('Kitchen','Rocki_ipaddress', dataholder.STRrocki_ipaddress)
    cfg.add_section('Nest')
    cfg.set('Nest','Pincode', dataholder.STRnest_pincode)
    cfg.set('Nest','Token', dataholder.STRnest_token)
    cfg.set('Nest','Token_expiry', dataholder.STRnest_tokenexp)
    #
    cfg.write(cfgfile)
    cfgfile.close()

def config_json(ARRobjects):
    data = ({'devices': config_json_room(ARRobjects), 'nest': config_json_nest()})
    with open('config.json', 'w') as outfile:
        outfile.write(json.dumps(data, outfile, indent=4, separators=(',', ': ')))
    return data

def config_json_room(ARRobjects):
    DICTrooms={}
    x=0
    while x<len(ARRobjects):
        DICTgroups={}
        y=0
        while y<len(ARRobjects[x][1]):
            DICTdevices={}
            z=0
            while z<len(ARRobjects[x][1][y][1]):
                #
                object=ARRobjects[x][1][y][1][z]
                #
                if isinstance(object, object_LGTV):
                    DICTdevices[object.getName()] = {'type':'lgtv',
                                                     'ipaddress':object.getIP(),
                                                     'pairingkey':object.getPairingkey(),
                                                     'usetvguide':object.getTvguide_use()}
                elif isinstance(object, object_TIVO):
                    DICTdevices[object.getName()] = {'type':'tivo',
                                                          'ipaddress':object.getIP(),
                                                          'mak':object.getAccesskey(),
                                                          'usetvguide':object.getTvguide_use()}
                #
                z+=1
            print DICTdevices
            DICTgroups[ARRobjects[x][1][y][0]] = DICTdevices
            y+=1
        DICTrooms[ARRobjects[x][0]] = DICTgroups
        x+=1
    return DICTrooms

def config_json_nest():
    return {'pincode': dataholder.STRnest_pincode, 'token': dataholder.STRnest_token, 'tokenexpiry': dataholder.STRnest_tokenexp}

'''
******** Example JSON ********
{"devices":
    [
    {"lounge":
        [
        {"TV":
            [
            {"LGTV":
                {
                "type": "lgtv",
                "ipaddress": dataholder.STRloungetv_lgtv_ipaddress,
                "pairingkey": dataholder.STRloungetv_lgtv_pairkey
                "usetvguide": true/false
                }
            },
            {"TIVO":
                {
                "type": "tivo",
                "ipaddress": dataholder.STRloungetv_tivo_ipaddress,
                "mak": dataholder.STRloungetv_tivo_mak
                "usetvguide": true/false
                }
            }
            ]
        },
        {
        "Music":
            [
            ]
        }
        ]
    },
"nest":
    {
    "pincode": "xxxxxx",
    "token": "45678-gfsas-2354656u-hgfds-eretry",
    "tokenexpiry", "xx/xx/xxxx xx:xx:xx"
    }
}
'''