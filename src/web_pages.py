from urllib import urlopen
from web_menu import html_menu
from web_users import html_users
from web_tvlistings import html_listings_user_and_all
from web_devices import _create_device_page


def create_login():
    return urlopen('web/header.html').read().encode('utf-8') + \
           html_users() + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_home(user, arr_devices):
    body = urlopen('web/index.html').read().encode('utf-8')
    return urlopen('web/header.html').read().encode('utf-8') + \
           html_menu(user, arr_devices, body) + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_about(user, arr_devices):
    body = urlopen('web/about.html').read().encode('utf-8')
    return urlopen('web/header.html').read().encode('utf-8') +\
           html_menu(user, arr_devices, body) + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_tvguide(user, arr_devices, listings):
    body = urlopen('web/tvguide.html').read().encode('utf-8').format(listings=html_listings_user_and_all(listings, device_url=False, user=user))
    return urlopen('web/header.html').read().encode('utf-8') +\
           html_menu(user, arr_devices, body) + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_device(user, tvlistings, arr_devices, group_name, device_name):
    body = urlopen('web/comp_alert.html').read().encode('utf-8') +\
           _create_device_page(user, tvlistings, arr_devices, group_name, device_name)
    return urlopen('web/header.html').read().encode('utf-8') +\
           html_menu(user, arr_devices, body) + \
           urlopen('web/footer.html').read().encode('utf-8')