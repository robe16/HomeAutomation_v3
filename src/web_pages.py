from urllib import urlopen
from web_menu import html_menu
from web_users import html_users
from web_tvlistings import listings_html, html_listings_user_and_all


def create_login():
    return urlopen('web/header.html').read().encode('utf-8') + \
           html_users() + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_home(user, theme, arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') + \
           html_menu(user, theme, arr_objects) + \
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
    device = None
    device_url = False
    str_devicehtml = ""
    while x < len(list_objects):
        str_devicehtml += _html_build_device_panels(list_objects[x], room, group)
        if list_objects[x].getTvguide_use():
            chan_current = list_objects[x].getChan()
            device = list_objects[x]
            device_url = "device/{}/{}/{}".format(room, group, list_objects[x].getName().replace(" ", "")).lower()
            tvguide = True
        x += 1
    if tvguide:
        html_tvguide = html_listings_user_and_all (listings,
                                                   room=room,
                                                   group=group,
                                                   device_url=device_url,
                                                   device=device,
                                                   chan_current=chan_current,
                                                   user=user)
        return urlopen('web/header.html').read().encode('utf-8') + \
               html_menu(user, theme, arr_objects) + \
               urlopen('web/comp_alert.html').read().encode('utf-8').format(body="-") + \
               urlopen('web/group_with-tvguide.html').read().encode('utf-8').format(room=room,
                                                                                    roomgroup=room + group,
                                                                                    devices=str_devicehtml,
                                                                                    tvguide=html_tvguide) + \
               urlopen('web/footer.html').read().encode('utf-8')
    else:
        return urlopen('web/header.html').read().encode('utf-8') + \
               html_menu(user, theme, arr_objects) + \
               urlopen('web/comp_alert.html').read().encode('utf-8').format(body="-") + \
               urlopen('web/group_no-tvguide.html').read().encode('utf-8').format(room=room,
                                                                                  roomgroup=room + group,
                                                                                  devices=str_devicehtml) + \
               urlopen('web/footer.html').read().encode('utf-8')


def create_tvguide(user, theme, listings, arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') +\
           html_menu(user, theme, arr_objects) + \
           urlopen('web/tvguide.html').read().encode('utf-8').format(listings=html_listings_user_and_all(listings, device_url=False, user=user)) + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_about(user, theme, arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') +\
           html_menu(user, theme, arr_objects) + \
           urlopen('web/about.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


def _html_build_device_panels (device, room, group):
    device_url = "device/{}/{}/{}".format(room, group, device.getName().replace(" ", "")).lower()
    if device.getLogo:
        str_panel = "<img src=\"/img/logo/{}\" style=\"height:25px;\"/> {}".format(device.getLogo(),
                                                                                   device.getName())
    else:
        str_panel = device.getName()
    str_objhtml = urlopen(('web/{}').format(device.getHtml())).read().encode('utf-8').format(url=device_url)
    str_devicehtml = urlopen('web/comp_panel.html').read().encode('utf-8').format(title=str_panel,
                                                                                   body=str_objhtml)
    str_devicehtml += "<br>"
    return str_devicehtml