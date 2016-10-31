from urllib import urlopen
from config_users import get_userrole, get_userimage
from list_devices import get_device_logo

from config_devices import get_cfg_idlist_structures, get_cfg_idlist_rooms, get_cfg_idlist_devices, get_cfg_idlist_accounts
from config_devices import get_cfg_structure_name, get_cfg_room_name, get_cfg_device_name, get_cfg_account_name
from config_devices import get_cfg_device_type, get_cfg_account_type
from config_devices import get_cfg_device_detail, get_cfg_account_detail


def html_menu(user):
    return html_menu_lhs() +\
           _html_menu_rhs(user) +\
           urlopen('web/cmd_alert.html').read().encode('utf-8')



def html_menu_lhs():
    #
    html = ''
    #
    s_list = get_cfg_idlist_structures()
    s_num = 0
    t = 0
    #
    while s_num < len(s_list):
        #
        html += '<span class="sidebar_divider box-shadow"></span>'
        #
        a_list = get_cfg_idlist_accounts(s_list[s_num])
        a_num = 0
        #
        while a_num < len(a_list):
            #
            label = get_cfg_account_name(s_list[s_num], a_list[a_num])
            img = get_device_logo(get_cfg_account_type(s_list[s_num], a_list[a_num]))
            #
            html += urlopen('web/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/account/{structure_id}/{account_id}').format(structure_id=s_list[s_num],
                                                                                                                                                           account_id=a_list[a_num]),
                                                                                                  id='{structure_id}_{account_id}'.format(structure_id=s_list[s_num],
                                                                                                                                          account_id=a_list[a_num]),
                                                                                                  cls='',
                                                                                                  name=label,
                                                                                                  img=img)

            #
            t += 1
            a_num += 1
        #
        r_list = get_cfg_idlist_rooms(s_list[s_num])
        r_num = 0
        #
        while r_num < len(r_list):
            d_list = get_cfg_idlist_devices(s_list[s_num], r_list[r_num])
            d_num = 0
            #
            html += '<span class="sidebar_divider box-shadow"></span>'
            #
            html += urlopen('web/html_menu/menu_sidebar_title.html').read().encode('utf-8').\
                format(name=get_cfg_room_name(s_list[s_num], r_list[r_num]))
            #
            while d_num < len(d_list):
                #
                label = get_cfg_device_name(s_list[s_num], r_list[r_num], d_list[d_num])
                img = get_device_logo(get_cfg_device_type(s_list[s_num], r_list[r_num], d_list[d_num]))
                #
                html += urlopen('web/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/device/{structure_id}/{room_id}/{device_id}').format(structure_id=s_list[s_num],
                                                                                                                                                                       room_id=r_list[r_num],
                                                                                                                                                                       device_id=d_list[d_num]),
                                                                                                      id='{structure_id}_{room_id}_{device_id}'.format(structure_id=s_list[s_num],
                                                                                                                                                       room_id=r_list[r_num],
                                                                                                                                                       device_id=d_list[d_num]),
                                                                                                      cls='',
                                                                                                      name=label,
                                                                                                      img=img)
                d_num += 1
            #
            r_num += 1
        #
        s_num += 1
    #
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