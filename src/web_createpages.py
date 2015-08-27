from urllib import urlopen
from enum_remoteLGTV import LSTremote_lgtv
from tvlisting import ARRsortlistings

def create_home():
    return urlopen('web/header.html').read().encode('utf-8')+\
           urlopen('web/index.html').read().encode('utf-8')+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_loungetv(listings):
    if listings:
        return urlopen('web/header.html').read().encode('utf-8')+\
               urlopen('web/alert.html').read().encode('utf-8')+\
               urlopen('web/loungetv.html').read().encode('utf-8').format(_lgtv(), _tivo(), urlopen('web/tvguide-data.html').read().encode('utf-8').format(_listings(listings)))+\
               urlopen('web/footer.html').read().encode('utf-8')
    else:
        return urlopen('web/header.html').read().encode('utf-8')+\
               urlopen('web/alert.html').read().encode('utf-8')+\
               urlopen('web/loungetv.html').read().encode('utf-8').format(_lgtv(), _tivo(), urlopen('web/tvguide-nodata.html').read().encode('utf-8'))+\
               urlopen('web/footer.html').read().encode('utf-8')

def create_tvguide(listings):
    if listings:
        return urlopen('web/header.html').read().encode('utf-8')+\
               urlopen('web/alert.html').read().encode('utf-8')+\
               urlopen('web/tvguide.html').read().encode('utf-8').format(urlopen('web/tvguide-data.html').read().encode('utf-8').format(_listings(listings)))+\
               urlopen('web/footer.html').read().encode('utf-8')
    else:
        return urlopen('web/header.html').read().encode('utf-8')+\
               urlopen('web/alert.html').read().encode('utf-8')+\
               urlopen('web/tvguide.html').read().encode('utf-8').format(urlopen('web/tvguide-nodata.html').read().encode('utf-8'))+\
               urlopen('web/footer.html').read().encode('utf-8')

def create_settings(clientID, STRnest_pincode, random):
    nesturl = ("https://home.nest.com/login/oauth2?client_id=" + clientID + "&state=" + "26GA-" + random)
    pincode = ("value=\""+STRnest_pincode+"\"") if bool(STRnest_pincode) else ""
    return urlopen('web/header.html').read().encode('utf-8')+\
           urlopen('web/alert.html').read().encode('utf-8')+\
           urlopen('web/settings.html').read().encode('utf-8').format(nesturl, pincode)+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_about():
    return urlopen('web/header.html').read().encode('utf-8')+\
           urlopen('web/about.html').read().encode('utf-8')+\
           urlopen('web/footer.html').read().encode('utf-8')

def _lgtv():
    return urlopen('web/loungetv-lgtv.html').read().encode('utf-8')

def _tivo():
    return urlopen('web/loungetv-tivo.html').read().encode('utf-8')

def _listings(listings):
    STRlistings = ""
    for x in range(len(listings)):
        STRlistings+=(_listingsrow(x, listings[x]))
    return STRlistings

def _listingsrow(x, item):
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
    return urlopen('web/tvguide-row.html').read().encode('utf-8').format(color, item[2], item[0], now, next, item[3], item[4])

def buttons_lgtv(room):
        comms = LSTremote_lgtv
        STRbuttons = "<div>"
        for x in range(len(comms)):
            STRbuttons+=(urlopen('web/button.html').read().encode('utf-8')).format(("/device/{}/lgtv/{}").format(room, comms[x][0]), "btn-default", comms[x][0])
        STRbuttons+="</div>"
        return STRbuttons