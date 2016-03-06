from urllib import urlopen
from tvlisting import returnnownext
from config_users import get_userchannels
from datetime import datetime


def html_listings_user_and_all (listings, device=None, group_name =False, device_name =False, chan_current=False, user=False):
    #
    html_tvguide = '<p style="text-align: right">Last updated {timestamp}</p>'.format(timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    #
    html_tvguide_all = _listings_html(listings,
                                      group_name = group_name,
                                      device_name = device_name,
                                      device = device,
                                      chan_current = chan_current)
    user_channels = get_userchannels(user)
    #
    if listings and user_channels:
        temp_listings=[]
        for i in listings:
            if i.name() in user_channels:
                temp_listings.append(i)
        html_tvguide_user = _listings_html(temp_listings,
                                           device = device,
                                           group_name = group_name,
                                           device_name = device_name,
                                           chan_current = chan_current,
                                           user = user)
        html_tvguide += urlopen('web/user_tabs.html').read().encode('utf-8').format(title_user=str(user)+'\'s favourites',
                                                                                   title_all='All channels',
                                                                                   body_user=html_tvguide_user,
                                                                                   body_all=html_tvguide_all)
    else:
        html_tvguide += html_tvguide_all
    #
    return html_tvguide


def _listings_html(listings, device=None, group_name =False, device_name=False, chan_current=False, user=False):
    if listings:
        if group_name and device_name:
            script = '<script>setTimeout(function () {getChannel(\'/command?group=' + str(group_name) + '&device=' + str(device_name) + '&command=getchannel\', true);}, 10000);</script>'
        else:
            script = ''
        return urlopen('web/html_tvguide/tvguide-data.html').read().encode('utf-8').format(script=script,
                                                                                           style='<style>tr.highlight {border:2px solid #FFBF47;border-radius=7px}</style>',
                                                                                           listings=_listings(listings, device=device, group_name=group_name, device_name=device_name, chan_current=chan_current, user=user))
    else:
        if group_name and device_name:
            device_query = '?device={device}&group={group}'.format(group = group_name, device = device_name)
        else:
            device_query = ''
        script = ('\r\n<script>\r\n' +
                  'setTimeout(function () {\r\n' +
                  'checkListings(\'/web/tvguide' + device_query + '\');\r\n' +
                  '}, 5000);\r\n' +
                  '</script>\r\n')
        return urlopen('web/html_tvguide/tvguide-nodata.html').read().encode('utf-8').format(script=script,
                                                                                             type='alert-danger',
                                                                                             body='<strong>An error has occurred!!</strong> The programme listings are still being retrieved - please wait and refresh shortly.')


def _listings(listings, device=None, chan_current=False, group_name=False, device_name=False, user=False):
    STRlistings = ""
    x = 0
    for lstg in listings:
        if lstg.getEnabled():
            STRlistings += _listingsrow(x, lstg, device, chan_current, group_name, device_name, user=user)
            x += 1
    return STRlistings


def _listingsrow(x, channelitem, device, chan_current, group_name=False, device_name=False, user=False, last=False):
    #
    try:
        channo = channelitem.devicekeys(device.getType())
    except:
        channo = False
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
    if bool(chan_current) and channo == chan_current:
        chan_highlight = ' highlight'
    else:
        chan_highlight = ''
    # If last item, add class text to add bottom border to row
    if last:
        item_last = ' tbl_border'
    else:
        item_last = ''
    # If device can change channel, add 'go' button
    if group_name and device_name and channo:
        go = urlopen('web/html_tvguide/tvguide-row_go.html').read().encode('utf-8').format(group=group_name,
                                                                                           device=device_name,
                                                                                           channo=channo)
    else:
        go = ''
    # Create element id, including user name if required (user name prevents duplication of id names within page)
    if user:
        chan_id = str(user).lower()+'_'
    chan_id += channelitem.name().replace(' ', '').lower()
    #
    return urlopen('web/html_tvguide/tvguide-row.html').read().encode('utf-8').format(id=('chan' + str(channo)),
                                                                                      chan_id=chan_id,
                                                                                      cls_highlight=chan_highlight,
                                                                                      cls_lastitem=item_last,
                                                                                      color=color,
                                                                                      imgtype=channelitem.type(),
                                                                                      imgchan=channelitem.logo(),
                                                                                      channame=channelitem.name(),
                                                                                      now=now,
                                                                                      next=next,
                                                                                      blurb=blurb,
                                                                                      go=go)