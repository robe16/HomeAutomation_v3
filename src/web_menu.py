import json
from urllib import urlopen
from config_users import get_usertheme, get_userrole, get_userimage


def html_menu(user):
    theme_navbar = _user_theme(user)
    user_image = _user_image(user)
    settings = _user_settings(user)
    return urlopen('web/menu.html').read().encode('utf-8').format(theme_navbar=theme_navbar,
                                                                  menus=_menudrops(),
                                                                  settings=settings,
                                                                  user=user,
                                                                  user_image=user_image)


def _menudrops():
    #
    with open('config_devices.json', 'r') as data_file:
        data = json.load(data_file)
    #
    STRhtml = ""
    for devicegroup in data:
        name = devicegroup['group']
        STRhtml += urlopen('web/menu_button.html').read().encode('utf-8').format(id=name.lower().replace(" ",""),
                                                                                 href='/web/devices/'+name.lower().replace(" ",""),
                                                                                 label=name)
    return STRhtml


def _user_theme(user):
    if get_usertheme(user) == "dark":
        return "navbar-inverse"
    else:
        return "navbar-default"


def _user_settings(user):
    if get_userrole(user) == "admin":
        return urlopen('web/menu_settings.html').read().encode('utf-8')
    else:
        return ""


def _user_image(user):
    return get_userimage(user)