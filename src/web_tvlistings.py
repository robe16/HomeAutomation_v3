from urllib import urlopen
from tvlisting import returnnownext

def get_tvlistings_for_device(listings, arr_objects, room, group, user=""):
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
                        device_url = "device/{room}/{group}/{name}".format(room=room,
                                                                           group=group,
                                                                           name=LSTobjects[x].getName().replace(" ", "")).lower()
                        if arr_objects[x][1][y][1][z].getTvguide_use:
                            chan_current = arr_objects[x][1][y][1][z].getChan()
                        z += 1
                y += 1
        x += 1
    #
    return _listings_html(listings, device_url, chan_current=chan_current, room=room, group=group, user=user)


def _listings_html(listings, deviceurl, device=False, chan_current=False, room=False, group=False, user=False):
    if listings:
        script = ""
        if room and group:
            script = "<script>setTimeout(function () {getChannel('/" + deviceurl + "/getchannel', true);}, 10000);</script>"
        return urlopen('web/tvguide-data.html').read().encode('utf-8').format(script=script,
                                                                              style="<style>tr.highlight {border:2px solid #FFBF47;border-radius=7px}</style>",
                                                                              listings=_listings(listings, device, deviceurl, chan_current, user=user))
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


def _listings(listings, device, deviceurl, chan_current, user=False):
    STRlistings = ""
    x = 0
    while x < len(listings):
        lstg = listings[x]
        STRlistings += _listingsrow(x, lstg, device, deviceurl, chan_current, user=user)
        x += 1
    return STRlistings


# TODO - entire section to redo in line with new chan object
def _listingsrow(x, channelitem, device, deviceurl, chan_current, user=False):
    #
    try:
        chan = channelitem.devicekeys(device.getType())
    except:
        chan = False
    #
    now = "-"
    next = "-"
    blurb = ""
    chan_id = ""
    #
    try:
        if channelitem and channelitem.getListings():
            for k, v in channelitem.getListings().items():
                nownext = returnnownext(k, v)
                if nownext:
                    now = "{} {}".format(nownext[0]['starttime'], nownext[0]['title'])
                    next = "{} {}".format(nownext[1]['starttime'], nownext[1]['title'])
                    for a in range(0, 5):
                        if a > 0:
                            blurb += '<br>'
                        blurb += '<b>{start}-{end} {title}</b><br>{desc}<br>'.format(start=nownext[a]['starttime'],
                                                                        end=nownext[a]['endtime'],
                                                                        title=nownext[a]['title'],
                                                                        desc=nownext[a]['desc'])
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
        go_desc = "<td></td>"
    else:
        go = ""
        go_desc = ""
    if user:
        chan_id = str(user).lower()+"_"
    chan_id += channelitem.name().replace(" ", "").lower()
    return urlopen('web/tvguide-row.html').read().encode('utf-8').format(id=("chan" + str(chan)),
                                                                         chan_id=chan_id,
                                                                         cls=chan_highlight,
                                                                         color=color,
                                                                         imgtype=channelitem.type(),
                                                                         imgchan=channelitem.logo(),
                                                                         channame=channelitem.name(),
                                                                         now=now,
                                                                         next=next,
                                                                         blurb=blurb,
                                                                         go=go,
                                                                         go_desc=go_desc)