import json
import os
from urllib import urlopen


def settings_tvguide():
    #
    color_gen = 'primary'
    #
    return urlopen('web/html_settings/settings_tvguide.html').read().encode('utf-8').format(color_gen = color_gen,
                                                                                            channels = _settings_tvguide_items(color_gen))

def _settings_tvguide_items(color_gen):
    #
    html = ''
    rowcolor = '#ffffff'
    #
    with open(os.path.join('lists', 'list_channels.json'), 'r') as data_file:
        data = json.load(data_file)
    data_channels = data["channels"]
    #
    for chan in data_channels:
        #
        chan_id = chan['name'].replace(' ', '').lower()
        chkd_gen = 'checked' if chan['enabled'] else ''
        # Create alternating row colours
        rowcolor = '#e8e8e8' if rowcolor == '#ffffff' else '#ffffff'
        #
        html += urlopen('web/html_settings/settings_tvguide_item.html').read().encode('utf-8').format(chan_id = chan_id,
                                                                                                      rowcolor = rowcolor,
                                                                                                      color_gen = color_gen,
                                                                                                      channame = chan['name'],
                                                                                                      imgtype = chan['type'],
                                                                                                      imgchan = chan['logo'],
                                                                                                      disabled_gen = '',
                                                                                                      chkd_gen = chkd_gen)
    #
    return html