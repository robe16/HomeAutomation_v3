from urllib import urlopen
from web_menu import html_menu
from web_create_login import html_users
from web_tvlistings import html_listings_user_and_all
from tvlisting_getfromqueue import _check_tvlistingsqueue


def create_login():
    return urlopen('web/header.html').read().encode('utf-8').format(title='Login') + \
           html_users() + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_home(user):
    body = urlopen('web/index.html').read().encode('utf-8')
    return urlopen('web/header.html').read().encode('utf-8').format(title='Home') + \
           html_menu(user) +\
           urlopen('web/body.html').read().encode('utf-8').format(header='', body=body) +\
           urlopen('web/footer.html').read().encode('utf-8')


def create_about(user):
    body = urlopen('web/about.html').read().encode('utf-8')
    return urlopen('web/header.html').read().encode('utf-8').format(title='About') +\
           html_menu(user) +\
           urlopen('web/body.html').read().encode('utf-8').format(header='About', body=body) +\
           urlopen('web/footer.html').read().encode('utf-8')


def create_tvguide(user, listings):
    body = urlopen('web/html_tvguide/tvguide.html').read().encode('utf-8').format(listings=html_listings_user_and_all(listings,
                                                                                                                      user=user))
    return urlopen('web/header.html').read().encode('utf-8').format(title='TV Guide') +\
           html_menu(user) +\
           urlopen('web/body.html').read().encode('utf-8').format(header='TV Guide', body=body) +\
           urlopen('web/footer.html').read().encode('utf-8')


def create_device(user, body, title, header):
    # title = '{structure}: {room}: {device}'
    # title = '{structure}: {account}'
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title=title) +\
           html_menu(user) +\
           urlopen('web/body.html').read().encode('utf-8').format(header=header, body=body) +\
           urlopen('web/footer.html').read().encode('utf-8')