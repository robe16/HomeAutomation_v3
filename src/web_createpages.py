from urllib import urlopen
from tvlisting import sort_arrlistings_radiotimes


def create_home(ARRobjects):
    return _header(ARRobjects) + \
           urlopen('web/index.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


# TODO - entire section re listings to recode following use of channel object and dict
# TODO - device channel number from channel dict now using device type, to recode
def create_device_group(listings, arr_objects, room, group):
    #
    list_objects = None
    x = 0
    while x < len(arr_objects):
        if room == arr_objects[x][0].lower():
            y = 0
            while y < len(arr_objects[x][1]):
                if group == (arr_objects[x][1][y][0]).lower():
                    list_objects = arr_objects[x][1][y][1]
                y += 1
        x += 1
    #
    x = 0
    device_url = False
    chan_array_no = None
    chan_current = False
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
        if list_objects[x].getTvguide_use:
            chan_array_no = list_objects[x].getChan_array_no()
            chan_current = list_objects[x].getChan()
        x += 1
    if chan_array_no:
        return _header(arr_objects) + \
               urlopen('web/comp_alert.html').read().encode('utf-8') + \
               urlopen('web/group_with-tvguide.html').read().encode('utf-8').format(room=room,
                                                                                    roomgroup=room + group,
                                                                                    devices=str_devicehtml,
                                                                                    tvguide=_listings_html(listings,
                                                                                                           device_url,
                                                                                                           chan_array_no=chan_array_no,
                                                                                                           chan_current=chan_current,
                                                                                                           room=room,
                                                                                                           group=group)) + \
               urlopen('web/footer.html').read().encode('utf-8')
    else:
        return _header(arr_objects) + \
               urlopen('web/comp_alert.html').read().encode('utf-8') + \
               urlopen('web/group_no-tvguide.html').read().encode('utf-8').format(room=room,
                                                                                  roomgroup=room + group,
                                                                                  devices=str_devicehtml) + \
               urlopen('web/footer.html').read().encode('utf-8')


def create_tvguide(listings, ARRobjects):
    return _header(ARRobjects) + \
           urlopen('web/tvguide.html').read().encode('utf-8').format(listings=_listings_html(listings, False)) + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_settings_devices(ARRobjects):
    return _header(ARRobjects) + \
           urlopen('web/comp_alert.html').read().encode('utf-8') + \
           urlopen('web/settings_devices.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


# TODO
def create_settings_tvguide(listings, ARRobjects):
    return _header(ARRobjects) + \
           urlopen('web/comp_alert.html').read().encode('utf-8') + \
           urlopen('web/settings_tvguide.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_settings_nest(ARRobjects, clientID, STRnest_pincode, random):
    nesturl = ('https://home.nest.com/login/oauth2?client_id={}&state={}').format(clientID, random)
    pincode = (' value="{}"').format(STRnest_pincode) if bool(STRnest_pincode) else ''
    print STRnest_pincode
    return _header(ARRobjects) + \
           urlopen('web/comp_alert.html').read().encode('utf-8') + \
           urlopen('web/settings_nest.html').read().encode('utf-8').format(nesturl, pincode) + \
           urlopen('web/footer.html').read().encode('utf-8')


def create_about(ARRobjects):
    return _header(ARRobjects) + \
           urlopen('web/about.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


def get_tvlistings_for_device(listings, ARRobjects, room, group):
    chan_array_no = None
    chan_current = False
    device_url = False
    x = 0
    while x < len(ARRobjects):
        if room == (ARRobjects[x][0]).lower():
            y = 0
            while y < len(ARRobjects[x][1]):
                if group == (ARRobjects[x][1][y][0]).lower():
                    LSTobjects = ARRobjects[x][1][y][1]
                    z = 0
                    while z < len(LSTobjects):
                        device_url = "device/" + room + "/" + group + "/" + LSTobjects[x].getName().replace(" ",
                                                                                                            "").lower()
                        if ARRobjects[x][1][y][1][z].getTvguide_use:
                            chan_array_no = ARRobjects[x][1][y][1][z].getChan_array_no()
                            chan_current = ARRobjects[x][1][y][1][z].getChan()
                        z += 1
                y += 1
        x += 1
    #
    return _listings_html(listings, device_url, chan_array_no=chan_array_no, chan_current=chan_current, room=room,
                          group=group)


def _header(ARRobjects):
    return urlopen('web/header.html').read().encode('utf-8') % (_headerdrops(ARRobjects))


def _headerdrops(ARRobjects):
    x = 0
    STRhtml = ""
    while x < len(ARRobjects):
        room = (ARRobjects[x][0]).lower()
        items = ""
        y = 0
        while y < len(ARRobjects[x][1]):
            group = (ARRobjects[x][1][y][0]).lower()
            items += urlopen('web/header_dropdown_items.html').read().encode('utf-8').format((room + group),
                                                                                             room + '/' + group,
                                                                                             group.upper())
            y += 1
        STRhtml += urlopen('web/header_dropdown.html').read().encode('utf-8').format(room, room.capitalize(), items)
        x += 1
    return STRhtml


# TODO - entire section to redo in line with new chan object
def _listings_html(listings, device, chan_array_no=-1, chan_current=False, room=False, group=True):
    if listings:
        if room and group:
            script = (
                "<script>setTimeout(function () {getChannel('/" + device + "/getchannel', true);}, 10000);</script>")
        else:
            script = ""
        return urlopen('web/tvguide-data.html').read().encode('utf-8').format(script=script,
                                                                              style="<style>tr.highlight {border:2px solid #FFBF47;border-radius=7px}</style>",
                                                                              listings=_listings(listings, device,
                                                                                                 chan_array_no,
                                                                                                 chan_current))
    else:
        if room and group:
            script = ("<script>" +
                      "setTimeout(function () {checkListings();}, 5000);function checkListings(){" +
                      "var xmlHttp = new XMLHttpRequest();" +
                      "xmlHttp.open('GET', '/web/" + room + "/" + group + "?tvguide=True', false);" + \
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


def _listings(listings, device, chan_array_no, chan_current):
    STRlistings = ""
    for x in range(len(listings)):
        STRlistings += (_listingsrow(x, listings[x], device, chan_array_no, chan_current))
    return STRlistings


def _listingsrow(x, item, device, chan_array_no, chan_current):
    if item[5]:
        nownext = sort_arrlistings_radiotimes(item[5])
        now = ("{} {}").format(nownext[0][1], nownext[0][4])
        next = ("{} {}").format(nownext[1][1], nownext[1][4])
    else:
        now = "-"
        next = "-"
    if x % 2 == 0:
        color = "#e8e8e8"
    else:
        color = "#ffffff"
    if bool(chan_current) and item[4][chan_array_no] == chan_current:
        chan_highlight = "class=\"highlight\""
        # chan_highlight="; border: 2px solid #FFBF47; border-radius: 7px;"
    else:
        chan_highlight = ""
    if device and not chan_array_no == -1:
        go = urlopen('web/tvguide-row_go.html').read().encode('utf-8').format(device=device,
                                                                              channo=item[4][chan_array_no])
    else:
        go = ""
    return urlopen('web/tvguide-row.html').read().encode('utf-8').format(id=("chan" + str(item[4][chan_array_no])),
                                                                         cls=chan_highlight,
                                                                         color=color,
                                                                         imgtype=item[3],
                                                                         imgchan=item[2],
                                                                         channame=item[0],
                                                                         now=now,
                                                                         next=next,
                                                                         go=go)
