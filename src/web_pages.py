from urllib import urlopen
from web_menu import _menu
from web_users import html_users
from web_tvlistings import _listings_html
from config_users import get_userchannels


def create_login():
    return urlopen('web/header.html').read().encode('utf-8') + \
           html_users() + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_home(user, theme, arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') + \
           _menu(user, theme, arr_objects) + \
           urlopen('web/index.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_device_group(user, theme, listings, arr_objects, room, group):
    #
    tvguide = False
    list_objects = None
    x = 0
    while x < len(arr_objects):
        if room == arr_objects[x][0].lower():
            y = 0
            while y < len(arr_objects[x][1]):
                if group == arr_objects[x][1][y][0].lower():
                    list_objects = arr_objects[x][1][y][1]
                y += 1
        x += 1
    #
    x = 0
    chan_current = False
    devicetv = None
    devicetv_url = False
    str_devicehtml = ""
    while x < len(list_objects):
        device_url = "device/{}/{}/{}".format(room, group, list_objects[x].getName().replace(" ", "")).lower()
        if list_objects[x].getLogo:
            str_panel = "<img src=\"/img/logo/{}\" style=\"height:25px;\"/> {}".format(list_objects[x].getLogo(),
                                                                                       list_objects[x].getName())
        else:
            str_panel = list_objects[x].getName()
        str_objhtml = urlopen(('web/{}').format(list_objects[x].getHtml())).read().encode('utf-8').format(
            url=device_url)
        str_devicehtml += urlopen('web/comp_panel.html').read().encode('utf-8').format(title=str_panel,
                                                                                       body=str_objhtml)
        str_devicehtml += "<br>"
        if list_objects[x].getTvguide_use():
            chan_current = list_objects[x].getChan()
            devicetv = list_objects[x]
            devicetv_url = "device/{}/{}/{}".format(room, group, list_objects[x].getName().replace(" ", "")).lower()
            tvguide = True
        x += 1
    if tvguide:
        user_channels = get_userchannels(user)
        if user_channels:
            temp_listings=[]
            for i in listings:
                if i.name() in user_channels:
                    temp_listings.append(i)
            html_tvguide_all = _listings_html(listings,
                                              devicetv_url,
                                              device=devicetv,
                                              chan_current=chan_current,
                                              room=room,
                                              group=group)
            html_tvguide_user = _listings_html(temp_listings,
                                               devicetv_url,
                                               device=devicetv,
                                               chan_current=chan_current,
                                               room=room,
                                               group=group)
            html_tvguide = urlopen('web/user_tabs.html').read().encode('utf-8').format(title_all="All channels",
                                                                                       title_user=user+"'s favourites",
                                                                                       body_all=html_tvguide_all,
                                                                                       body_user=html_tvguide_user)
        else:
            html_tvguide = _listings_html(listings,
                                          devicetv_url,
                                          device=devicetv,
                                          chan_current=chan_current,
                                          room=room,
                                          group=group)
        return urlopen('web/header.html').read().encode('utf-8') + \
               _menu(user, theme, arr_objects) + \
               urlopen('web/comp_alert.html').read().encode('utf-8') + \
               urlopen('web/group_with-tvguide.html').read().encode('utf-8').format(room=room,
                                                                                    roomgroup=room + group,
                                                                                    devices=str_devicehtml,
                                                                                    tvguide=html_tvguide) + \
               urlopen('web/footer.html').read().encode('utf-8')
    else:
        return urlopen('web/header.html').read().encode('utf-8') +\
               _menu(user, theme, arr_objects) + \
               urlopen('web/comp_alert.html').read().encode('utf-8') + \
               urlopen('web/group_no-tvguide.html').read().encode('utf-8').format(room=room,
                                                                                  roomgroup=room + group,
                                                                                  devices=str_devicehtml) + \
               urlopen('web/footer.html').read().encode('utf-8')


def create_tvguide(user, theme, listings, arr_objects):
    #TODO TV favourites for users
    return urlopen('web/header.html').read().encode('utf-8') +\
           _menu(user, theme, arr_objects) + \
           urlopen('web/tvguide.html').read().encode('utf-8').format(listings=_listings_html(listings, False)) + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_about(user, theme, arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') +\
           _menu(user, theme, arr_objects) + \
           urlopen('web/about.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')