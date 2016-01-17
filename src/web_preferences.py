from urllib import urlopen
import os
import json
from config_users import get_userchannels

def _preference_tvguide(user):
    #
    color_gen = 'primary'
    color_usr = 'warning'
    #
    user_channels = get_userchannels(user)
    #
    if user_channels:
        usr_header = '<span class="label label-{color_usr}" style="font-weight: bold">{user}\'s favourites</span>'.format(user = user, color_usr = color_usr)
    else:
        usr_header = ''
    #
    pre_html = '<p align="center"><strong>Note:</strong> blah blah blah</p>'
    script_src = 'preferences_tvguide.js'
    btn_name = 'Update user preferences'
    #
    return urlopen('web/settings_tvguide.html').read().encode('utf-8').format(panel_title = 'User Preferences: TV Guide',
                                                                              pre_html = pre_html,
                                                                              script_src = script_src,
                                                                              btn_name = btn_name,
                                                                              color_gen = color_gen,
                                                                              usr_header = usr_header,
                                                                              listings = _preference_tvguide_items(user, user_channels, color_gen, color_usr))

def _preference_tvguide_items(user, user_channels, color_gen, color_usr):
    #
    with open(os.path.join('lists', 'list_channels.json'), 'r') as data_file:
        data = json.load(data_file)
    data_channels = data["channels"]
    html = ''
    rowcolor = '#ffffff'
    #
    for chan in data_channels:
        #
        chan_id = chan['name'].replace(' ', '').lower()
        chkd_gen = 'checked' if chan['enabled'] else ''
        # Create alternating row colours
        rowcolor = '#e8e8e8' if rowcolor == '#ffffff' else '#ffffff'
        #
        if user_channels:
            # Get if item is in user's preferences
            chkd_usr = ''
            for n in user_channels:
                if chan['name'].lower() == n.lower():
                    chkd_usr = 'checked'
                    break
            #
            html_usr_tgle = urlopen('web/settings_tvguide_toggle.html').read().encode('utf-8').format(chan_name = chan['name'],
                                                                                                      color_usr = color_usr,
                                                                                                      chkd_usr = chkd_usr)
        else:
            html_usr_tgle = ''
        #
        html += urlopen('web/settings_tvguide_item.html').read().encode('utf-8').format(chan_id = chan_id,
                                                                                        rowcolor = rowcolor,
                                                                                        color_gen = color_gen,
                                                                                        channame = chan['name'],
                                                                                        imgtype = chan['type'],
                                                                                        imgchan = chan['logo'],
                                                                                        disabled_gen = 'disabled=true',
                                                                                        chkd_gen = chkd_gen,
                                                                                        user_chan_toggle = html_usr_tgle)
    #
    return html