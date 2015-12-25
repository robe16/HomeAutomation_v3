from urllib import urlopen
from web_menu import _menu

def create_settings_devices(user, theme, arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') +\
           _menu(user, theme, arr_objects) + \
           urlopen('web/comp_alert.html').read().encode('utf-8') + \
           urlopen('web/settings_devices.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


# TODO
def create_settings_tvguide(user, theme, listings, arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') +\
           _menu(user, theme, arr_objects) + \
           urlopen('web/comp_alert.html').read().encode('utf-8') + \
           urlopen('web/settings_tvguide.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_settings_nest(user, theme, arr_objects, clientID, STRnest_pincode, random):
    nesturl = 'https://home.nest.com/login/oauth2?client_id={}&state={}'.format(clientID, random)
    pincode = ' value="{}"'.format(STRnest_pincode) if bool(STRnest_pincode) else ''
    print STRnest_pincode
    return urlopen('web/header.html').read().encode('utf-8') +\
           _menu(user, theme, arr_objects) + \
           urlopen('web/comp_alert.html').read().encode('utf-8') + \
           urlopen('web/settings_nest.html').read().encode('utf-8').format(nesturl, pincode) + \
           urlopen('web/footer.html').read().encode('utf-8')