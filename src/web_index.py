from urllib import urlopen
from enum_remoteLGTV import LSTremote_lgtv

def create_home():
    return urlopen('web/header.html').read().encode('utf-8')+\
           urlopen('web/index.html').read().encode('utf-8')+\
           urlopen('web/footer.html').read().encode('utf-8')

def create_loungetv():
    return urlopen('web/header.html').read().encode('utf-8')+\
           urlopen('web/loungetv.html').read().encode('utf-8') % (buttons_lgtv("lounge"))+\
           urlopen('web/footer.html').read().encode('utf-8')

def buttons_lgtv(room):
        comms = LSTremote_lgtv
        STRbuttons = "<div>"
        for x in range(len(comms)):
            STRbuttons+=(urlopen('web/button.html').read().encode('utf-8')).format(("/device/{}/lgtv/{}").format(room, comms[x][0]), "btn-default", comms[x][0])
        STRbuttons+="</div>"
        return STRbuttons