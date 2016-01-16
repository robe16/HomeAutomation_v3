from urllib import urlopen
from web_menu import html_menu
from web_users import html_users
from web_tvlistings import html_listings_user_and_all
from web_devices import _create_device_page

#TODO - change title to include house name (from config file - todo)

def create_login():
    return urlopen('web/header.html').read().encode('utf-8').format(title='Login') + \
           html_users() + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_home(user, arr_devices):
    body = urlopen('web/index.html').read().encode('utf-8')
    return urlopen('web/header.html').read().encode('utf-8').format(title='Home') + \
           html_menu(user, arr_devices) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')


def create_about(user, arr_devices):
    body = urlopen('web/about.html').read().encode('utf-8')
    return urlopen('web/header.html').read().encode('utf-8').format(title='About') +\
           html_menu(user, arr_devices) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')


def create_tvguide(user, arr_devices, listings):
    body = urlopen('web/tvguide.html').read().encode('utf-8').format(listings=html_listings_user_and_all(listings, device_url=False, user=user))
    return urlopen('web/header.html').read().encode('utf-8').format(title='TV Guide') +\
           html_menu(user, arr_devices) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')


def create_device(user, tvlistings, arr_devices, group_name, device_name):
    #
    device = False
    #
    for device_group in arr_devices:
        # Get group name - as some groups do not have a name, default this to '-'
        grp_name = device_group['name'] if not device_group['name'] == '' else '-'
        #
        if grp_name.lower().replace(' ','') == group_name:
            #
            for device_item in device_group['devices']:
                if device_item.getName().lower().replace(' ','') == device_name:
                    #
                    device = device_item
                    break
        if not device:
            break
    #
    body = urlopen('web/comp_alert.html').read().encode('utf-8').format(body='-') +\
           _create_device_page(user, tvlistings, device, group_name, device_name)
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title=grp_name + ': ' + device.getName()) +\
           html_menu(user, arr_devices) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')