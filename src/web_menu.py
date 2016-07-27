from urllib import urlopen
from config_users import get_userrole, get_userimage
from config_devices import get_device_json, count_groups, count_devices
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
    #
    grp_count = count_groups()
    grp_num = 0
    #
    while grp_num < grp_count:
        dvc_count = count_devices(grp_num)
        dvc_num = 0
        #
        html += '<span class="sidebar_divider box-shadow"></span>'
        #
        if not data[str(grp_num)]['name'] == '':
            name = data[str(grp_num)]['name']
            html += urlopen('web/html_menu/menu_sidebar_title.html').read().encode('utf-8').format(name=name)
        else:
            name = '-'
        #
        while dvc_num < dvc_count:
            #
            type = data[str(grp_num)]['devices'][str(dvc_num)]['device']
            label = data[str(grp_num)]['devices'][str(dvc_num)]['details']['name']
            img = get_device_logo(type)
            #
            html += urlopen('web/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/device/{group}/{device}').format(group=str(grp_num), device=str(dvc_num)),
                                                                                                  id='{}_{}'.format(str(grp_num), str(dvc_num)),
                                                                                                  cls='',
                                                                                                  name=label,
                                                                                                  img=img)
            dvc_num += 1
        #
        grp_num += 1
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