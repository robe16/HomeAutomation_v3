from urllib import urlopen
from web_menu import html_menu
from web_create_login import html_users
from web_tvlistings import html_listings_user_and_all
from web_devices import _create_device_page
from config_devices_create import create_device_object


def create_login():
    return urlopen('web/header.html').read().encode('utf-8').format(title='Login') + \
           html_users() + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_home(user):
    body = urlopen('web/index.html').read().encode('utf-8')
    return urlopen('web/header.html').read().encode('utf-8').format(title='Home') + \
           html_menu(user) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')


def create_about(user):
    body = urlopen('web/about.html').read().encode('utf-8')
    return urlopen('web/header.html').read().encode('utf-8').format(title='About') +\
           html_menu(user) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')


def create_tvguide(user, listings):
    body = urlopen('web/html_tvguide/tvguide.html').read().encode('utf-8').format(listings=html_listings_user_and_all(listings,
                                                                                                                      user=user))
    return urlopen('web/header.html').read().encode('utf-8').format(title='TV Guide') +\
           html_menu(user) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')


def create_device(user, tvlistings, group_name, device_name, request):
    #
    device = create_device_object(group_name, device_name)
    #
    if bool(device):
        body = _create_device_page(user, tvlistings, device, group_name, device_name)
    else:
        raise Exception
    #
    if request.query.body:
        return body
    #
    title = '{group}: {label}'.format(group=device.getGroup(), label=device.getLabel())
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title=title) +\
           html_menu(user) +\
           urlopen('web/body.html').read().encode('utf-8').format(body=body) +\
           urlopen('web/footer.html').read().encode('utf-8')