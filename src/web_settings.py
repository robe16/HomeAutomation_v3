from urllib import urlopen
import os
import json
from web_menu import html_menu
from config_users import get_userchannels


# TODO - redo code for new device config schema
def create_settings_devices(user, arr_devices):
    body = urlopen('web/settings_devices.html').read().encode('utf-8')
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title='Settings: Devices') +\
           html_menu(user, arr_devices, body) + \
           urlopen('web/footer.html').read().encode('utf-8')


# TODO
def create_settings_tvguide(user, arr_devices):
    body = urlopen('web/settings_tvguide.html').read().encode('utf-8').format(listings=_settings_tvguide_items(user))
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title='Settings: TV Guide') +\
           html_menu(user, arr_devices, body) + \
           urlopen('web/footer.html').read().encode('utf-8')


# TODO - now part of device settings pages (not dedicated)
def create_settings_nest(user, arr_devices, clientID, STRnest_pincode, random):
    nesturl = 'https://home.nest.com/login/oauth2?client_id={}&state={}'.format(clientID, random)
    pincode = ' value="{}"'.format(STRnest_pincode) if bool(STRnest_pincode) else ''
    #print STRnest_pincode
    body = urlopen('web/comp_alert.html').read().encode('utf-8').format(body="-") + \
           urlopen('web/settings_nest.html').read().encode('utf-8').format(nesturl, pincode)
    return urlopen('web/header.html').read().encode('utf-8') +\
           html_menu(user, arr_devices, body) + \
           urlopen('web/footer.html').read().encode('utf-8')




def _settings_tvguide_items(user):
    #
    with open(os.path.join('lists', 'list_channels.json'), 'r') as data_file:
        data = json.load(data_file)
    data_channels = data["channels"]
    #
    user_channels = get_userchannels(user)
    html = ''
    color = '#ffffff'
    #
    for chan in data_channels:
        #
        chan_id = chan['name'].replace(' ', '').lower()
        chkd_gen = 'checked' if chan['enabled'] else ''
        # Create alternating row colours
        color = '#e8e8e8' if color == '#ffffff' else '#ffffff'
        #
        if user_channels:
            # Get if item is in user's preferences
            chkd_usr = ''
            for n in user_channels:
                if chan['name'].lower() == n.lower():
                    chkd_usr = 'checked'
                    break
            #
            html_usr_tgle = '<input type="checkbox" id="{user}-{chan_id}" style="vertical-align: center;" data-on-color="success" {chkd_usr}>'.format(chan_id = chan_id, chkd_usr = chkd_usr, user = user.lower())
            html_usr_code = '$("[id=\'{user}-{chan_id}\']").bootstrapSwitch();'.format(chan_id = chan_id, user = user.lower())
        else:
            html_usr_tgle = ''
            html_usr_code = ''
        #
        html += urlopen('web/settings_tvguide_item.html').read().encode('utf-8').format(chan_id = chan_id,
                                                                                        color = color,
                                                                                        channame = chan['name'],
                                                                                        imgtype = chan['type'],
                                                                                        imgchan = chan['logo'],
                                                                                        chkd_gen = chkd_gen,
                                                                                        user_chan_toggle = html_usr_tgle,
                                                                                        html_usr_code = html_usr_code)
    #
    return html