import os
import json
import ast


def update_channellist(new_data):
    #
    # value 'data' passed through will be the new settings for channels being enabled/disabled
    #
    try:
        #
        with open(os.path.join('lists', 'list_channels.json'), 'r') as data_file:
            data = json.load(data_file)
            data_file.close()
        #
        new_data = ast.literal_eval(new_data)
        #
        x=0
        while x<len(data['channels']):
            if data['channels'][x]['name'].lower().replace(' ','') in new_data:
                data['channels'][x]['enabled'] = True
            else:
                data['channels'][x]['enabled'] = False
            x+=1
        #
        with open(os.path.join('lists', 'list_channels.json'), 'w+') as output_file:
            output_file.write(json.dumps(data, indent=4, separators=(',', ': ')))
            output_file.close()
        #
        return True
        #
    except:
        return False