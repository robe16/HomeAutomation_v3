from urllib import urlopen
from tvlisting import returnnownext


def create_home(arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') + \
           _menu(arr_objects) + \
           urlopen('web/index.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_device_group(listings, arr_objects, room, group):
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
        return urlopen('web/header.html').read().encode('utf-8') +\
               _menu(arr_objects) + \
               urlopen('web/comp_alert.html').read().encode('utf-8') + \
               urlopen('web/group_with-tvguide.html').read().encode('utf-8').format(room=room,
                                                                                    roomgroup=room + group,
                                                                                    devices=str_devicehtml,
                                                                                    tvguide=_listings_html(listings,
                                                                                                           devicetv_url,
                                                                                                           device=devicetv,
                                                                                                           chan_current=chan_current,
                                                                                                           room=room,
                                                                                                           group=group)) + \
               urlopen('web/footer.html').read().encode('utf-8')
    else:
        return urlopen('web/header.html').read().encode('utf-8') +\
               _menu(arr_objects) + \
               urlopen('web/comp_alert.html').read().encode('utf-8') + \
               urlopen('web/group_no-tvguide.html').read().encode('utf-8').format(room=room,
                                                                                  roomgroup=room + group,
                                                                                  devices=str_devicehtml) + \
               urlopen('web/footer.html').read().encode('utf-8')


def create_tvguide(listings, arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') +\
           _menu(arr_objects) + \
           urlopen('web/tvguide.html').read().encode('utf-8').format(listings=_listings_html(listings, False)) + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_settings_devices(arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') +\
           _menu(arr_objects) + \
           urlopen('web/comp_alert.html').read().encode('utf-8') + \
           urlopen('web/settings_devices.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


# TODO
def create_settings_tvguide(listings, arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') +\
           _menu(arr_objects) + \
           urlopen('web/comp_alert.html').read().encode('utf-8') + \
           urlopen('web/settings_tvguide.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_settings_nest(arr_objects, clientID, STRnest_pincode, random):
    nesturl = 'https://home.nest.com/login/oauth2?client_id={}&state={}'.format(clientID, random)
    pincode = ' value="{}"'.format(STRnest_pincode) if bool(STRnest_pincode) else ''
    print STRnest_pincode
    return urlopen('web/header.html').read().encode('utf-8') +\
           _menu(arr_objects) + \
           urlopen('web/comp_alert.html').read().encode('utf-8') + \
           urlopen('web/settings_nest.html').read().encode('utf-8').format(nesturl, pincode) + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_about(arr_objects):
    return urlopen('web/header.html').read().encode('utf-8') +\
           _menu(arr_objects) + \
           urlopen('web/about.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


def get_tvlistings_for_device(listings, arr_objects, room, group):
    chan_current = False
    device_url = False
    x = 0
    while x < len(arr_objects):
        if room == arr_objects[x][0].lower():
            y = 0
            while y < len(arr_objects[x][1]):
                if group == arr_objects[x][1][y][0].lower():
                    LSTobjects = arr_objects[x][1][y][1]
                    z = 0
                    while z < len(LSTobjects):
                        device_url = "device/{}/{}/{}".format(room, group,
                                                              LSTobjects[x].getName().replace(" ", "")).lower()
                        if arr_objects[x][1][y][1][z].getTvguide_use:
                            chan_current = arr_objects[x][1][y][1][z].getChan()
                        z += 1
                y += 1
        x += 1
    #
    return _listings_html(listings, device_url, chan_current=chan_current, room=room, group=group)


def _menu(arr_objects):
    return urlopen('web/menu.html').read().encode('utf-8') % (_headerdrops(arr_objects))


def _headerdrops(arr_objects):
    x = 0
    STRhtml = ""
    while x < len(arr_objects):
        room = arr_objects[x][0].lower()
        items = ""
        y = 0
        while y < len(arr_objects[x][1]):
            group = arr_objects[x][1][y][0].lower()
            items += urlopen('web/header_dropdown_items.html').read().encode('utf-8').format(room + group,
                                                                                             room + '/' + group,
                                                                                             group.upper())
            y += 1
        STRhtml += urlopen('web/header_dropdown.html').read().encode('utf-8').format(room, room.capitalize(), items)
        x += 1
    return STRhtml


def _listings_html(listings, deviceurl, device=False, chan_current=False, room=False, group=False):
    if listings:
        if room and group:
            script = "<script>setTimeout(function () {getChannel('/" + deviceurl + "/getchannel', true);}, 10000);</script>"
        else:
            script = ""
        return urlopen('web/tvguide-data.html').read().encode('utf-8').format(script=script,
                                                                              style="<style>tr.highlight {border:2px solid #FFBF47;border-radius=7px}</style>",
                                                                              listings=_listings(listings, device, deviceurl, chan_current))
    else:
        if room and group:
            script = ("<script>" +
                      "setTimeout(function () {checkListings();}, 5000);function checkListings(){" +
                      "var xmlHttp = new XMLHttpRequest();" +
                      "xmlHttp.open('GET', '/web/"+str(room)+"/"+str(group)+"?tvguide=True', false);" +
                      "xmlHttp.send(null);" +
                      "if (xmlHttp.status==200) {" +
                      "document.getElementById('alert-tvguide').remove();" +
                      "document.getElementById('tvguide-panelbody').innerHTML=xmlHttp.responseText}" +
                      "else {setTimeout(function () {checkListings();}, 5000);}" +
                      "}" +
                      "</script>")
        else:
            script = ""
        return urlopen('web/tvguide-nodata.html').read().encode('utf-8').format(script=script)


def _listings(listings, device, deviceurl, chan_current):
    STRlistings = ""
    x = 0
    while x < len(listings):
        lstg = listings[x]
        STRlistings += _listingsrow(x, lstg, device, deviceurl, chan_current)
        x += 1
    return STRlistings


# TODO - entire section to redo in line with new chan object
def _listingsrow(x, channelitem, device, deviceurl, chan_current):
    #
    try:
        chan = channelitem.devicekeys(device.getType())
    except:
        chan = False
    #
    now = "-"
    next = "-"
    #
    try:
        if channelitem and channelitem.getListings():
            for k, v in channelitem.getListings().items():
                nownext = returnnownext(k, v)
                if nownext:
                    now = "{} {}".format(nownext[0]['starttime'], nownext[0]['title'])
                    next = "{} {}".format(nownext[1]['starttime'], nownext[1]['title'])
                    break
    except:
        now = "-"
        next = "-"
    if x % 2 == 0:
        color = "#e8e8e8"
    else:
        color = "#ffffff"
    if bool(chan_current) and chan == chan_current:
        chan_highlight = "class=\"highlight\""
        # chan_highlight="; border: 2px solid #FFBF47; border-radius: 7px;"
    else:
        chan_highlight = ""
    if deviceurl and chan:
        go = urlopen('web/tvguide-row_go.html').read().encode('utf-8').format(device=deviceurl,
                                                                              channo=chan)
    else:
        go = ""
    return urlopen('web/tvguide-row.html').read().encode('utf-8').format(id=("chan" + str(chan)),
                                                                         cls=chan_highlight,
                                                                         color=color,
                                                                         imgtype=channelitem.type(),
                                                                         imgchan=channelitem.logo(),
                                                                         channame=channelitem.name(),
                                                                         now=now,
                                                                         next=next,
                                                                         go=go)
