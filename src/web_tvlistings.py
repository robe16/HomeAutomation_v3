from urllib import urlopen
from tvlisting import returnnownext
from config_users import get_userchannels
from config_devices import get_device_config_detail
from datetime import datetime


def html_listings_user_and_all (listings, group_name=False, device_name=False, user=False):
    #
    html_tvguide = '<p style="text-align: right">Last updated {timestamp}</p>'.format(timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    #
    if not listings:
        html_tvguide += _html_no_listings(group_name=group_name, device_name=device_name)
        return html_tvguide
    #
    categories = listings['categories']
    all_count = 0
    html_nav_user = ''
    html_nav_all = ''
    html_content = ''
    #
    # Build HTML code for 'user' TV channels
    #
    user_channels = get_userchannels(user)
    #
    if listings and user_channels:
        #
        all_count += 1
        active = 'active' if all_count == 1 else ''
        #
        html_nav_user += urlopen('web/pills_nav.html').read().encode('utf-8').format(active=active,
                                                                                    category=str(user).lower(),
                                                                                    title=str(user)+'\'s favourites')
        #
        temp_listings=[]
        for cat in categories:
            for l in listings['channels'][cat]:
                if l.name() in user_channels:
                    temp_listings.append(l)
        #
        body = _html_listings(temp_listings,
                              group_name = group_name,
                              device_name = device_name,
                              user = user)
        #
        html_content += urlopen('web/pills_contents.html').read().encode('utf-8').format(active=active,
                                                                                         category=str(user).lower(),
                                                                                         body=body)
        #
        #chan_current = chan_current,
    #
    # Build HTML code for 'all' TV channels
    #
    for cat in categories:
        all_count += 1
        active = 'active' if all_count == 1 else ''
        #
        html_nav_all += urlopen('web/pills_nav.html').read().encode('utf-8').format(active=active,
                                                                                    category=cat.lower(),
                                                                                    title=cat)
        #
        body = _html_listings(listings['channels'][cat],
                              group_name = group_name,
                              device_name = device_name)
        #
        html_content += urlopen('web/pills_contents.html').read().encode('utf-8').format(active=active,
                                                                                         category=cat.lower(),
                                                                                         body=body)
        #
    #
    # If user channels available, change categories into dropdown menu
    if user_channels:
        html_nav_all = urlopen('web/pills_nav_dropdown.html').read().encode('utf-8').format(title='All Channels',
                                                                                            dropdowns=html_nav_all)
    #
    # Combine pills for 'user' and 'all' channel listings
    html_nav = html_nav_user + html_nav_all
    #
    html_tvguide += urlopen('web/pills_parent.html').read().encode('utf-8').format(nav=html_nav,
                                                                                   content=html_content)
    #
    return html_tvguide


def _html_no_listings(group_name=False, device_name=False):
    #
    if group_name and device_name:
        device_query = '?group={group_name}&device={device_name}'.format(group_name=group_name, device_name=device_name)
    else:
        device_query = ''
    #
    script = ('\r\n<script>\r\n' +
              'setTimeout(function () {\r\n' +
              'checkListings(\'/web/tvguide' + device_query + '\');\r\n' +
              '}, 5000);\r\n' +
              '</script>\r\n')
    body = '<strong>An error has occurred!!</strong> The programme listings are still being retrieved - please wait and refresh shortly.'
    #
    return urlopen('web/html_tvguide/tvguide-nodata.html').read().encode('utf-8').format(script=script,
                                                                                         type='alert-danger',
                                                                                         body=body)


def _html_listings(listings, group_name=False, device_name=False, chan_current=False, user=False):
    #
    if group_name and device_name:
        script = '<script>setTimeout(function () {getChannel(\'/command?group=' + str(group_name) +\
                 '&device=' + str(device_name) +\
                 '&command=getchannel\', true);}, 10000);</script>'
    else:
        script = ''
    style = '<style>tr.highlight {border:2px solid #FFBF47;border-radius=7px}</style>'
    lstngs = _listings(listings,
                       group_name=group_name,
                       device_name=device_name,
                       chan_current=chan_current,
                       user=user)
    #
    return urlopen('web/html_tvguide/tvguide-data.html').read().encode('utf-8').format(script=script,
                                                                                       style=style,
                                                                                       listings=lstngs)


def _listings(listings, group_name=False, device_name=False, chan_current=False, user=False):
    STRlistings = ""
    x = 0
    for lstg in listings:
        STRlistings += _listingsrow(x, lstg, chan_current, group_name, device_name, user=user)
        x += 1
    return STRlistings


def _listingsrow(x, channelitem, chan_current, group_name=False, device_name=False, user=False, last=False):
    #
    try:
        channo = channelitem.devicekeys(get_device_config_detail(group_name,
                                                                 device_name,
                                                                 'type'))
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
    chan_id += channelitem.category().replace(' ', '').lower()
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