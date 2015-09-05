from urllib import urlopen
from tvlisting import ARRsortlistings

def create_home(ARRobjects):
    return _header(ARRobjects)+\
           urlopen('web/index.html').read().encode('utf-8')+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_device_group(listings, ARRobjects, room, group):
    #
    LSTobjects=None
    x=0
    while x<len(ARRobjects):
        if room==(ARRobjects[x][0]).lower():
            y=0
            while y<len(ARRobjects[x][1]):
                if group==(ARRobjects[x][1][y][0]).lower():
                    LSTobjects=ARRobjects[x][1][y][1]
                y+=1
        x+=1
    #
    x=0
    device_url=False
    chan_array_no=None
    chan_current=False
    STRdevicehtml=""
    while x<len(LSTobjects):
        device_url="device/"+room+"/"+group+"/"+LSTobjects[x].getName().replace(" ", "").lower()
        if LSTobjects[x].getLogo:
            STRpanel=("<img src=\"/img/logo/{}\" style=\"height:25px;\"/> {}").format(LSTobjects[x].getLogo(), LSTobjects[x].getName())
        else:
            STRpanel=LSTobjects[x].getName()
        STRobjhtml=urlopen(('web/{}').format(LSTobjects[x].getHtml())).read().encode('utf-8').format(url=device_url)
        STRdevicehtml+=urlopen('web/comp_panel.html').read().encode('utf-8').format(title=STRpanel,
                                                                                    body=STRobjhtml)
        STRdevicehtml+="<br>"
        if LSTobjects[x].getTvguide_use:
            chan_array_no=LSTobjects[x].getChan_array_no()
            chan_current=LSTobjects[x].getChan()
        x+=1
    if not chan_array_no==None:
        return _header(ARRobjects)+\
               urlopen('web/comp_alert.html').read().encode('utf-8')+\
               urlopen('web/group_with-tvguide.html').read().encode('utf-8').format(room=room,
                                                                                    roomgroup=room+group,
                                                                                    devices=STRdevicehtml,
                                                                                    tvguide=_listings_html(listings, device_url, chan_array_no=chan_array_no, chan_current=chan_current))+\
               urlopen('web/footer.html').read().encode('utf-8')
    else:
        return _header(ARRobjects)+\
               urlopen('web/comp_alert.html').read().encode('utf-8')+\
               urlopen('web/group_no-tvguide.html').read().encode('utf-8').format(room=room,
                                                                                  roomgroup=room+group,
                                                                                  devices=STRdevicehtml)+\
               urlopen('web/footer.html').read().encode('utf-8')

def create_tvguide(listings, ARRobjects):
    return _header(ARRobjects)+\
           urlopen('web/tvguide.html').read().encode('utf-8').format(listings=_listings_html(listings, False))+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_settings_devices(ARRobjects):
    return _header(ARRobjects)+\
           urlopen('web/comp_alert.html').read().encode('utf-8')+\
           urlopen('web/settings_devices.html').read().encode('utf-8')+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_settings_nest(ARRobjects, clientID, STRnest_pincode, random):
    nesturl = ("https://home.nest.com/login/oauth2?client_id=" + clientID + "&state=" + "26GA-" + random)
    pincode = ("value=\""+STRnest_pincode+"\"") if bool(STRnest_pincode) else ""
    return _header(ARRobjects)+\
           urlopen('web/comp_alert.html').read().encode('utf-8')+\
           urlopen('web/settings_nest.html').read().encode('utf-8').format(nesturl, pincode)+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_about(ARRobjects):
    return _header(ARRobjects)+\
           urlopen('web/about.html').read().encode('utf-8')+\
           urlopen('web/footer.html').read().encode('utf-8')

def _header(ARRobjects):
    return urlopen('web/header.html').read().encode('utf-8') % (_headerdrops(ARRobjects))

def _headerdrops(ARRobjects):
    x=0
    STRhtml=""
    while x<len(ARRobjects):
        room=(ARRobjects[x][0]).lower()
        items=""
        y=0
        while y<len(ARRobjects[x][1]):
            group=(ARRobjects[x][1][y][0]).lower()
            items+=urlopen('web/header_dropdown_items.html').read().encode('utf-8').format((room+group), room+'/'+group, group.upper())
            y+=1
        STRhtml+=urlopen('web/header_dropdown.html').read().encode('utf-8').format(room, room.capitalize(), items)
        x+=1
    return STRhtml

def _listings_html (listings, device, chan_array_no=-1, chan_current=False):
    if listings:
        return urlopen('web/tvguide-data.html').read().encode('utf-8').format(style="<style>tr.highlight {border:2px solid #FFBF47;border-radius=7px}</style>",
                                                                              listings=_listings(listings, device, chan_array_no, chan_current))
    else:
        return urlopen('web/tvguide-nodata.html').read().encode('utf-8')

def _listings(listings, device, chan_array_no, chan_current):
    STRlistings = ""
    for x in range(len(listings)):
        STRlistings+=(_listingsrow(x, listings[x], device, chan_array_no, chan_current))
    return STRlistings

def _listingsrow(x, item, device, chan_array_no, chan_current):
    if item[5]:
        nownext = ARRsortlistings(item[5])
        now = ("{} {}").format(nownext[0][1], nownext[0][4])
        next = ("{} {}").format(nownext[1][1], nownext[1][4])
    else:
        now = "-"
        next = "-"
    if x % 2==0:
        color="#e8e8e8"
    else:
        color="#ffffff"
    if bool(chan_current) and item[4][chan_array_no]==chan_current:
        chan_highlight="class=\"highlight\""
        #chan_highlight="; border: 2px solid #FFBF47; border-radius: 7px;"
    else:
        chan_highlight=""
    if device and not chan_array_no==-1:
        go = urlopen('web/tvguide-row_go.html').read().encode('utf-8').format(device=device,
                                                                              channo=item[4][chan_array_no],
                                                                              trid="chan"+str(item[4][chan_array_no]))
    else:
        go = ""
    return urlopen('web/tvguide-row.html').read().encode('utf-8').format(id=("chan"+str(item[4][chan_array_no])),
                                                                         cls=chan_highlight,
                                                                         color=color,
                                                                         imgtype=item[3],
                                                                         imgchan=item[2],
                                                                         channame=item[0],
                                                                         now=now,
                                                                         next=next,
                                                                         go=go)