from urllib import urlopen
from web_menu import html_menu
from web_settings import _settings_tvguide


# TODO - redo code for new device config schema
def create_settings_devices(user, arr_devices):
    body = urlopen('web/settings_devices.html').read().encode('utf-8')
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title='Settings: Devices') +\
           html_menu(user, arr_devices) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')


# TODO
def create_settings_tvguide(user, arr_devices):
    body = _settings_tvguide(user)
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title='Settings: TV Guide') +\
           html_menu(user, arr_devices) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')


# TODO - now part of device settings pages (not dedicated)
def create_settings_nest(user, arr_devices, clientID, STRnest_pincode, random):
    nesturl = 'https://home.nest.com/login/oauth2?client_id={}&state={}'.format(clientID, random)
    pincode = ' value="{}"'.format(STRnest_pincode) if bool(STRnest_pincode) else ''
    #print STRnest_pincode
    body = urlopen('web/comp_alert.html').read().encode('utf-8').format(body="-") + \
           urlopen('web/settings_nest.html').read().encode('utf-8').format(nesturl, pincode)
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title='[DEPRECIATED] Settings: Nest Account') +\
           html_menu(user, arr_devices) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')