from urllib import urlopen
from tvlisting import returnnownext
from config_users import get_userchannels
from datetime import datetime


#def html_listings_user_and_all (listings, arr_objects=None, group=False, device_url=None, device=None, chan_current=False, user=False):
def html_listings_user_and_all (listings, device=None, device_url=None, chan_current=False, user=False):
    html_tvguide = '<p style="text-align: right">Last updated {timestamp}</p>'.format(timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    html_tvguide_all = _listings_html(listings,
                                      device_url=device_url,
                                      device=device,
                                      chan_current=chan_current)
    user_channels = get_userchannels(user)
    if listings and user_channels:
        temp_listings=[]
        for i in listings:
            if i.name() in user_channels:
                temp_listings.append(i)
        html_tvguide_user = _listings_html(temp_listings,
                                           device=device,
                                           device_url=device_url,
                                           chan_current=chan_current,
                                           user=user)
        html_tvguide += urlopen('web/user_tabs.html').read().encode('utf-8').format(title_user=str(user)+'\'s favourites',
                                                                                   title_all='All channels',
                                                                                   body_user=html_tvguide_user,
                                                                                   body_all=html_tvguide_all)
    else:
        html_tvguide += html_tvguide_all
    #
    return html_tvguide


def _listings_html(listings, device=None, device_url=False, chan_current=False, user=False):
    if listings:
        if device_url:
            script = '<script>setTimeout(function () {getChannel(\'/' + device_url + '/getchannel\', true);}, 10000);</script>'
        else:
            script = ''
        return urlopen('web/tvguide-data.html').read().encode('utf-8').format(script=script,
                                                                              style='<style>tr.highlight {border:2px solid #FFBF47;border-radius=7px}</style>',
                                                                              listings=_listings(listings, device=device, device_url=device_url, chan_current=chan_current, user=user))
    else:
        try:
            chan = listings[0].devicekeys(device.getType())
        except:
            chan = False
        if device_url and chan:
            script = ('<script>' +
                      'setTimeout(function () {checkListings();}, 5000);function checkListings(){' +
                      'var xmlHttp = new XMLHttpRequest();' +
                      'xmlHttp.open(\'GET\', \'/web/device/'+device_url+'?tvguide=True\', false);' +
                      'xmlHttp.send(null);' +
                      'if (xmlHttp.status==200) {' +
                      'document.getElementById(\'alert-tvguide\').remove();' +
                      'document.getElementById(\'tvguide-panelbody\').innerHTML=xmlHttp.responseText}' +
                      'else {setTimeout(function () {checkListings();}, 5000);}' +
                      '}' +
                      '</script>')
        else:
            script = ''
        return urlopen('web/tvguide-nodata.html').read().encode('utf-8').format(script=script,
                                                                                type='alert-danger',
                                                                                body='<strong>An error has occurred!!</strong> The programme listings are still being retrieved - please wait and refresh shortly.')


def _listings(listings, device=None, device_url=None, chan_current=False, user=False):
    STRlistings = ""
    x = 0
    for lstg in listings:
        if lstg.getEnabled():
            STRlistings += _listingsrow(x, lstg, device, device_url, chan_current, user=user)
            x += 1
    return STRlistings


def _listingsrow(x, channelitem, device, device_url, chan_current, user=False):
    #
    try:
        chan = channelitem.devicekeys(device.getType())
    except:
        chan = False
    #
    now = '-'
    next = '-'
    blurb = ''
    chan_id = ''
    #
    try:
        if channelitem and channelitem.getListings():
            for k, v in channelitem.getListings().items():
                nownext = returnnownext(k, v)
                if nownext:
                    now = '{} {}'.format(nownext[0]['starttime'], nownext[0]['title'])
                    next = '{} {}'.format(nownext[1]['starttime'], nownext[1]['title'])
                    for a in range(0, 5):
                        if a > 0:
                            blurb += '<br>'
                        blurb += '<b>{start}-{end} {title}</b><br>{desc}<br>'.format(start=nownext[a]['starttime'],
                                                                                     end=nownext[a]['endtime'],
                                                                                     title=nownext[a]['title'],
                                                                                     desc=nownext[a]['desc'])
                    break
    except:
        now = '-'
        next = '-'
    # Create alternating row colours
    if x % 2 == 0:
        color = '#e8e8e8'
    else:
        color = '#ffffff'
    # If current channel, create element class text for highlighting
    if bool(chan_current) and chan == chan_current:
        chan_highlight = 'class="highlight"'
    else:
        chan_highlight = ""
    # If device can change channel, add 'go' button
    if device_url and chan:
        go = urlopen('web/tvguide-row_go.html').read().encode('utf-8').format(device=device_url,
                                                                              channo=chan)
        go_desc = '<td></td>'
    else:
        go = ''
        go_desc = ''
    # Create element id, including user name if required (user name prevents duplication of id names within page)
    if user:
        chan_id = str(user).lower()+'_'
    chan_id += channelitem.name().replace(' ', '').lower()
    #
    return urlopen('web/tvguide-row.html').read().encode('utf-8').format(id=('chan' + str(chan)),
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