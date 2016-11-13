from urllib import urlopen

from src.config.devices.config_devices import get_cfg_device_type, get_cfg_account_type
from src.config.devices.config_devices import get_cfg_idlist_rooms, get_cfg_idlist_devices, get_cfg_idlist_accounts
from src.config.devices.config_devices import get_cfg_room_name, get_cfg_device_name, get_cfg_account_name
from src.config.users.config_users import get_userrole, get_userimage
from src.lists.devices.list_devices import get_device_logo


def html_menu(user):
    return html_menu_lhs() +\
           _html_menu_rhs(user) +\
           urlopen('web/html/cmd_alert.html').read().encode('utf-8')



def html_menu_lhs():
    #
    html = ''
    #
    t = 0
    #
    a_list = get_cfg_idlist_accounts()
    a_num = 0
    #
    while a_num < len(a_list):
        #
        html += '<span class="sidebar_divider box-shadow"></span>'
        #
        label = get_cfg_account_name(a_list[a_num])
        img = get_device_logo(get_cfg_account_type(a_list[a_num]))
        #
        html += urlopen('web/html/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/account/{account_id}').format(account_id=a_list[a_num]),
                                                                                              id='{account_id}'.format(account_id=a_list[a_num]),
                                                                                              cls='',
                                                                                              name=label,
                                                                                              img=img)

        #
        t += 1
        a_num += 1
    #
    r_list = get_cfg_idlist_rooms()
    r_num = 0
    #
    while r_num < len(r_list):
        d_list = get_cfg_idlist_devices(r_list[r_num])
        d_num = 0
        #
        html += '<span class="sidebar_divider box-shadow"></span>'
        #
        html += urlopen('web/html/html_menu/menu_sidebar_title.html').read().encode('utf-8').\
            format(name=get_cfg_room_name(r_list[r_num]))
        #
        while d_num < len(d_list):
            #
            label = get_cfg_device_name(r_list[r_num], d_list[d_num])
            img = get_device_logo(get_cfg_device_type(r_list[r_num], d_list[d_num]))
            #
            html += urlopen('web/html/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/device/{room_id}/{device_id}').format(room_id=r_list[r_num],
                                                                                                                                                    device_id=d_list[d_num]),
                                                                                                  id='{room_id}_{device_id}'.format(room_id=r_list[r_num],
                                                                                                                                    device_id=d_list[d_num]),
                                                                                                  cls='',
                                                                                                  name=label,
                                                                                                  img=img)
            d_num += 1
        #
        r_num += 1
    #
    return urlopen('web/html/html_menu/menu_lhs.html').read().encode('utf-8').format(menu=html)


def _html_menu_rhs(user):
    #user = user if user != False else 'Guest'
    user_image = _user_image(user)
    html_settings = _user_settings(user)
    return urlopen('web/html/html_menu/menu_rhs.html').read().encode('utf-8').format(settings=html_settings,
                                                                                user=user,
                                                                                user_image=user_image)


def _user_settings(user):
    if get_userrole(user) == "admin":
        return urlopen('web/html/html_menu/menu_settings.html').read().encode('utf-8')
    else:
        return ""


def _user_image(user):
    return get_userimage(user)