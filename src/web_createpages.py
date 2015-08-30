from urllib import urlopen
from tvlisting import ARRsortlistings

def create_home():
    return _header()+\
           urlopen('web/index.html').read().encode('utf-8')+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_device_group(listings, LSTobjects):
    x=0
    tvguide_device=False
    chan_array_no=None
    STRdevicehtml=""
    while x<len(LSTobjects):
        if LSTobjects[x].getLogo:
            STRpanel=("<img src=\"/img/logo/{}\" style=\"height:25px;\"/> {}").format(LSTobjects[x].getLogo(), LSTobjects[x].getName())
        else:
            STRpanel=LSTobjects[x].getName()
        STRobjhtml=urlopen(('web/{}').format(LSTobjects[x].getHtml())).read().encode('utf-8')
        STRdevicehtml+=urlopen('web/comp_panel.html').read().encode('utf-8').format(STRpanel, STRobjhtml)
        STRdevicehtml+="<br>"
        if LSTobjects[x].getTvguide_use:
            tvguide_device=LSTobjects[x].getGroup()+"/"+LSTobjects[x].getDevice()
            chan_array_no=LSTobjects[x].getChan_array_no()
        x+=1
    return _header()+\
           urlopen('web/comp_alert.html').read().encode('utf-8')+\
           urlopen('web/loungetv.html').read().encode('utf-8').format(STRdevicehtml, _listings_html(listings, tvguide_device, chan_array_no=chan_array_no))+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_tvguide(listings):
    return _header()+\
           urlopen('web/tvguide.html').read().encode('utf-8').format(_listings_html(listings, False))+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_settings_rooms():
    return _header()+\
           urlopen('web/comp_alert.html').read().encode('utf-8')+\
           urlopen('web/settings_rooms.html').read().encode('utf-8')+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_settings_devices():
    return _header()+\
           urlopen('web/comp_alert.html').read().encode('utf-8')+\
           urlopen('web/settings_devices.html').read().encode('utf-8')+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_settings_nest(clientID, STRnest_pincode, random):
    nesturl = ("https://home.nest.com/login/oauth2?client_id=" + clientID + "&state=" + "26GA-" + random)
    pincode = ("value=\""+STRnest_pincode+"\"") if bool(STRnest_pincode) else ""
    return _header()+\
           urlopen('web/comp_alert.html').read().encode('utf-8')+\
           urlopen('web/settings_nest.html').read().encode('utf-8').format(nesturl, pincode)+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_about():
    return _header()+\
           urlopen('web/about.html').read().encode('utf-8')+\
           urlopen('web/footer.html').read().encode('utf-8')

def _header():
    return urlopen('web/header.html').read().encode('utf-8') % (_headerdrops())

def _headerdrops():
    return urlopen('web/header_dropdown.html').read().encode('utf-8')

def _listings_html (listings, device, chan_array_no=-1):
    if listings:
        return urlopen('web/tvguide-data.html').read().encode('utf-8').format(_listings(listings, device, chan_array_no))
    else:
        return urlopen('web/tvguide-nodata.html').read().encode('utf-8')

def _listings(listings, device, chan_array_no):
    STRlistings = ""
    for x in range(len(listings)):
        STRlistings+=(_listingsrow(x, listings[x], device, chan_array_no))
    return STRlistings

def _listingsrow(x, item, device, chan_array_no):
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
    if device and not chan_array_no==-1:
        go = urlopen('web/tvguide-row_go.html').read().encode('utf-8').format(device, item[4][chan_array_no])
    else:
        go = ""
    return urlopen('web/tvguide-row.html').read().encode('utf-8').format(color, item[3], item[2], item[0], now, next, go)