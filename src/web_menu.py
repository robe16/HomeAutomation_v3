from urllib import urlopen
from config_users import get_userrole, get_userimage
from config_devices import get_device_json
from list_devices import get_device_logo


def html_menu(user):
    return html_menu_lhs() +\
           _html_menu_rhs(user) +\
           urlopen('web/cmd_alert.html').read().encode('utf-8')


def html_menu_lhs():
    #
    html = ''
    #
    data = get_device_json()
    #
    grp_keys = data.keys()
    for grp in grp_keys:
        #
        html += '<span class="sidebar_divider box-shadow"></span>'
        #
        if not data[grp]['group'] == '':
            name = data[grp]['group']
            html += urlopen('web/html_menu/menu_sidebar_title.html').read().encode('utf-8').format(name=name)
        else:
            name = '-'
        #
        dvc_keys = data[grp]['devices'].keys()
        for dvc in dvc_keys:
            #
            type = data[grp]['devices'][dvc]['device']
            label = data[grp]['devices'][dvc]['details']['name']
            img = get_device_logo(type)
            #
            html += urlopen('web/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/device/{group}/{device}').format(group=name.lower().replace(" ",""), device=label.lower().replace(" ","")),
                                                                                                  id='{}_{}'.format(name.lower().replace(' ',''), label.lower().replace(' ','')),
                                                                                                  cls='',
                                                                                                  name=label,
                                                                                                  img=img)
    return urlopen('web/html_menu/menu_lhs.html').read().encode('utf-8').format(menu=html)


def _html_menu_rhs(user):
    #user = user if user != False else 'Guest'
    user_image = _user_image(user)
    html_settings = _user_settings(user)
    return urlopen('web/html_menu/menu_rhs.html').read().encode('utf-8').format(settings=html_settings,
                                                                                user=user,
                                                                                user_image=user_image)


def _user_settings(user):
    if get_userrole(user) == "admin":
        return urlopen('web/html_menu/menu_settings.html').read().encode('utf-8')
    else:
        return ""


def _user_image(user):
    return get_userimage(user)