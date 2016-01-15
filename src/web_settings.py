from urllib import urlopen
from web_menu import html_menu


# TODO - redo code for new device config schema
def create_settings_devices(user, arr_devices):
    body = urlopen('web/comp_alert.html').read().encode('utf-8').format(body="-") + \
           urlopen('web/settings_devices.html').read().encode('utf-8')
    return urlopen('web/header.html').read().encode('utf-8').format(title='Settings: Devices') +\
           html_menu(user, arr_devices, body) + \
           urlopen('web/footer.html').read().encode('utf-8')


# TODO
def create_settings_tvguide(user, arr_devices, listings):
    body = urlopen('web/comp_alert.html').read().encode('utf-8').format(body="-") + \
           urlopen('web/settings_tvguide.html').read().encode('utf-8')
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