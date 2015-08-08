from urllib import urlopen
from enum_remoteLGTV import LSTremote_lgtv
from tvlisting import getall_listings, getall_xmllistings, get_xmllistings

def create_home():
    return urlopen('web/header.html').read().encode('utf-8')+\
           urlopen('web/index.html').read().encode('utf-8')+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_loungetv():
    return urlopen('web/header.html').read().encode('utf-8')+\
           urlopen('web/alert.html').read().encode('utf-8')+\
           urlopen('web/loungetv.html').read().encode('utf-8').format(_lgtv(), _tivo())+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_tvguide(listings):
    return urlopen('web/header.html').read().encode('utf-8')+\
           urlopen('web/alert.html').read().encode('utf-8')+\
           urlopen('web/tvguide.html').read().encode('utf-8').format(_listings(listings))+\
           urlopen('web/footer.html').read().encode('utf-8')

def _lgtv():
    return urlopen('web/loungetv-lgtv.html').read().encode('utf-8')

def _tivo():
    return urlopen('web/loungetv-tivo.html').read().encode('utf-8')

def _listings(listings):
    STRlistings = ""
    for x in range(len(listings)):
        STRlistings+=(_listingsrow(listings[x]))
    return STRlistings

def _listingsrow(item):
    return urlopen('web/tvguide-row.html').read().encode('utf-8').format(item[4], item[2], item[0], "now", "next", item[3])

def buttons_lgtv(room):
        comms = LSTremote_lgtv
        STRbuttons = "<div>"
        for x in range(len(comms)):
            STRbuttons+=(urlopen('web/button.html').read().encode('utf-8')).format(("/device/{}/lgtv/{}").format(room, comms[x][0]), "btn-default", comms[x][0])
        STRbuttons+="</div>"
        return STRbuttons