from urllib import urlopen
from web_menu import html_menu
from web_users import html_users
from web_tvlistings import html_listings_user_and_all


def create_login():
    return urlopen('web/header.html').read().encode('utf-8') + \
           html_users() + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_home(user):
    return urlopen('web/header.html').read().encode('utf-8') + \
           html_menu(user) + \
           urlopen('web/index.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_tvguide(user, listings):
    return urlopen('web/header.html').read().encode('utf-8') +\
           html_menu(user) + \
           urlopen('web/tvguide.html').read().encode('utf-8').format(listings=html_listings_user_and_all(listings, device_url=False, user=user)) + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_about(user):
    return urlopen('web/header.html').read().encode('utf-8') +\
           html_menu(user) + \
           urlopen('web/about.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')