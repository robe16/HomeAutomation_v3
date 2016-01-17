import os
import json

#TODO - enabling/disabling on master channel json list
#TODO - updaing user config file with user favourites (different def required?)
def update_channellist(data):
    #
    # value 'data' passed through will be the new settings for channels being enabled/disabled
    #
    with open(os.path.join('lists', 'list_channels.json'), 'r') as data_file:
        data = json.load(data_file)
    data_channels = data["channels"]
    #