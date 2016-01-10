import json
import os


def read_config_nest():
    with open(os.path.join('config', 'config_nest.json'), 'r') as data_file:
        data = json.load(data_file)
    return read_json_nest(data)


def read_json_nest(dataX):
    if not isinstance(dataX, dict):
        data = json.loads(dataX)
    else:
        data = dataX
    #
    ARRnestData = []
    ARRnestData.append(data['nest']['pincode'])
    ARRnestData.append(data['nest']['token'])
    ARRnestData.append(data['nest']['tokenexpiry'])
    return ARRnestData


def write_config_nest(ARRnestData):
    try:
        with open(os.path.join('config', 'config_nest.json'), 'w') as outfile:
            outfile.write(json.dumps(create_json_nest(ARRnestData), outfile, indent=4, separators=(',', ': ')))
        return True
    except:
        return False


def create_json_nest(ARRnestData):
    return {'nest': {'pincode': ARRnestData[0], 'token': ARRnestData[1], 'tokenexpiry': ARRnestData[2]}}


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