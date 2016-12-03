from urllib import urlopen

from web_create_login import html_users
from web_menu import html_menu
from web_tvlistings import html_listings_user_and_all


def create_login():
    return urlopen('web/html/header.html').read().encode('utf-8').format(title='Login') + \
           html_users() + \
           urlopen('web/html/footer.html').read().encode('utf-8')


def create_home(user):
    body = urlopen('web/html/index.html').read().encode('utf-8')
    return urlopen('web/html/header.html').read().encode('utf-8').format(title='Home') + \
           html_menu(user) +\
           urlopen('web/html/body.html').read().encode('utf-8').format(header='', body=body) +\
           urlopen('web/html/footer.html').read().encode('utf-8')


def create_about(user):
    body = urlopen('web/html/about.html').read().encode('utf-8')
    return urlopen('web/html/header.html').read().encode('utf-8').format(title='About') +\
           html_menu(user) +\
           urlopen('web/html/body.html').read().encode('utf-8').format(header='About', body=body) +\
           urlopen('web/html/footer.html').read().encode('utf-8')

from src.bundles.info_services.weather_metoffice import metoffice

def create_weather(user):
    body = ''
    #
    # TODO - create object to get html - temporary until create queue for item
    m = metoffice.info_metoffice()
    body = m.getHtml(user)
    #
    return urlopen('web/html/header.html').read().encode('utf-8').format(title='Weather') +\
           html_menu(user) +\
           urlopen('web/html/body.html').read().encode('utf-8').format(header='Weather', body=body) +\
           urlopen('web/html/footer.html').read().encode('utf-8')


def create_tvguide(user, listings):
    body = urlopen('web/html/html_tvguide/tvguide.html').read().encode('utf-8').format(listings=html_listings_user_and_all(listings,
                                                                                                                           user=user))
    return urlopen('web/html/header.html').read().encode('utf-8').format(title='TV Guide') +\
           html_menu(user) +\
           urlopen('web/html/body.html').read().encode('utf-8').format(header='TV Guide', body=body) +\
           urlopen('web/html/footer.html').read().encode('utf-8')


def create_device(user, body, title, header):
    # title = '{room}: {device}'
    # title = '{account}'
    #
    return urlopen('web/html/header.html').read().encode('utf-8').format(title=title) +\
           html_menu(user) +\
           urlopen('web/html/body.html').read().encode('utf-8').format(header=header, body=body) +\
           urlopen('web/html/footer.html').read().encode('utf-8')