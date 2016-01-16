from urllib import urlopen
from config_users import get_usertheme, get_userrole, get_userimage


def create_test(user, arr_devices):
    body = '<div class="container-fluid">'+\
                '<div class="row">'+\
                    '<div class="col-lg-12">'+\
                        '<h1>Test Page</h1><br>'+\
                    '</div>'+\
                '</div>'+\
            '</div>'
    return urlopen('web/header.html').read().encode('utf-8') +\
           _html_menu_rhs(user) +\
           html_sidebar(arr_devices, body + urlopen('web/footer.html').read().encode('utf-8'))


def html_sidebar(arr_devices, body):
    # Use passed through arr_devices as opposed to using json as require
    # device objects that have details regarding to images/logos
    html = ''
    for device_group in arr_devices:
        html += '<span class="sidebar_divider"></span>'
        if not device_group['name'] == '':
            html += urlopen('web/menu_sidebar_title.html').read().encode('utf-8').format(name=device_group['name'])
        for device in device_group['devices']:
            html += urlopen('web/menu_sidebar_item.html').read().encode('utf-8').format(href='',
                                                                                        id='{}_{}'.format(device_group['name'].lower().replace(' ',''), device.getName().lower().replace(' ','')),
                                                                                        cls='',
                                                                                        name=device.getName(),
                                                                                        img=device.getLogo())
    return urlopen('web/menu_lhs.html').read().encode('utf-8').format(menu=html, body=body)


def _html_menu_rhs(user):
    user_image = _user_image(user)
    return urlopen('web/menu_rhs.html').read().encode('utf-8').format(user=user,
                                                                      settings='',
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