from urllib import urlopen
from web_menu import html_menu
from web_preferences import _preference_tvguide


def create_preference_tvguide(user, arr_devices):
    body = _preference_tvguide(user)
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title='User Preferences: TV Guide') +\
           html_menu(user, arr_devices) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')