from urllib import urlopen
from config_users import get_usertheme, get_userrole, get_userimage


# theme_navbar = _user_theme(user)
# user_image = _user_image(user)


def html_menu(user, arr_devices):
    return html_menu_lhs(arr_devices) + _html_menu_rhs(user)


def html_menu_lhs(arr_devices):
    # Use passed through arr_devices as opposed to using json as require
    # device objects that have details regarding to images/logos
    html = ''
    for device_group in arr_devices:
        html += '<span class="sidebar_divider box-shadow"></span>'
        if not device_group['name'] == '':
            name = device_group['name']
            html += urlopen('web/menu_sidebar_title.html').read().encode('utf-8').format(name=name)
        else:
            name = '-'
        for device in device_group['devices']:
            html += urlopen('web/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/device/{group}/{device}').format(group=name.lower().replace(" ",""),
                                                                                                                                      device=device.getName().lower().replace(" ","")),
                                                                                        id='{}_{}'.format(device_group['name'].lower().replace(' ',''), device.getName().lower().replace(' ','')),
                                                                                        cls='',
                                                                                        name=device.getName(),
                                                                                        img=device.getLogo())
    return urlopen('web/menu_lhs.html').read().encode('utf-8').format(menu=html)


def _html_menu_rhs(user):
    user_image = _user_image(user)
    html_settings = _user_settings(user)
    return urlopen('web/menu_rhs.html').read().encode('utf-8').format(settings=html_settings,
                                                                      user=user,
                                                                      user_image=user_image)


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