from urllib import urlopen

from src.config.devices.config_devices import get_cfg_device_type
from src.config.users.config_users import get_userchannels
from src.lists.channels.list_channels import *


def html_channels_user_and_all (room_id=False, device_id=False, user=False, chan_current=False, package=False):
    #
    if not read_list_channels():
        return _html_no_channels()
    #
    categories = get_channel_categories()
    user_channels = get_userchannels(user)
    #
    html_channels = ''
    #
    if room_id and device_id:
        html_channels += '<script>setTimeout(function () {getChannel(\'/command/device/' + str(room_id) + \
                         '/' + str(device_id) + \
                         '?command=getchannel\', true);}, 10000);</script>'
    #
    all_count = 0
    html_nav_user = ''
    html_nav_all = ''
    html_content = ''
    #
    # Build HTML code for 'user' TV channels
    #
    if user_channels:
        #
        all_count += 1
        active = 'active' if all_count == 1 else ''
        #
        html_nav_user += urlopen('web/pills_nav.html').read().encode('utf-8').format(active=active,
                                                                                    category=str(user).lower(),
                                                                                    title=str(user)+'\'s favourites')
        #
        temp_cats=[]
        temp_channels=[]
        for cat in categories:
            chan = get_channel_cat_list(cat)
            for c in chan:
                if c['name'] in user_channels:
                    temp_cats.append(cat)
                    temp_channels.append(c)
        #
        body = _html_channels(temp_cats,
                              temp_channels,
                              room_id=room_id,
                              device_id=device_id,
                              user=user,
                              chan_current=chan_current,
                              package=package)
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
        body = _html_channels(cat,
                              get_channel_cat_list(cat),
                              room_id=room_id,
                              device_id=device_id,
                              chan_current=chan_current,
                              package=package)
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
    html_channels += urlopen('web/pills_parent.html').read().encode('utf-8').format(nav=html_nav,
                                                                                   content=html_content)
    #
    return html_channels


def _html_no_channels():
    #
    body = '<strong>An error has occurred!!</strong> The list of channels on the server is empty. Please check server setup.'
    #
    return urlopen('web/comp_alert.html').read().encode('utf-8').format(type='alert-danger',
                                                                        body=body)


def _html_channels(category, channels, room_id=False, device_id=False, chan_current=False, user=False, package=False):
    #
    header = '{user}\'s favourites'.format(user=user) if user else category
    #
    html_chans = _channels(category,
                           channels,
                           room_id=room_id,
                           device_id=device_id,
                           chan_current=chan_current,
                           user=user,
                           package=package)
    #
    return urlopen('web/html_tvguide/tvguide-grid.html').read().encode('utf-8').format(header=header,
                                                                                       html_chans=html_chans)


def _channels(category, channels, room_id=False, device_id=False, chan_current=False, user=False, package=False):
    html = ''
    x = 0
    for chan in channels:
        #
        use = False
        res = False
        #
        if isinstance(category, list):
            cat = category[x]
        else:
            cat = category
        #
        if bool(package):
            use = False
            if package[0]=='freeview':
                if get_channel_item_res_freeview(cat, chan['name'], 'hd'):
                    res = 'hd'
                    use = True
                elif get_channel_item_res_freeview(cat, chan['name'], 'sd'):
                    res = 'sd'
                    use = True
            else:
                device_package_name = package[0]
                device_package_level = package[1]
                #
                hd_package = get_channel_item_res_package(cat, chan['name'], 'hd', device_package_name)
                if bool(hd_package):
                    for p in device_package_level:
                        if p in hd_package:
                            res = 'hd'
                            use = True
                if not bool(hd_package) or not use:
                    sd_package = get_channel_item_res_package(cat, chan['name'], 'sd', device_package_name)
                    if bool(sd_package):
                        for p in device_package_level:
                            if p in sd_package:
                                res = 'sd'
                                use = True
        #
        if use:
            if (x+1) == len(channels):
                last = True
            else:
                last = False
            html += _channelitem(x, cat, chan, res, chan_current, room_id, device_id, user=user)
            x += 1
    #
    return html


def _channelitem(x, category, channel, res, chan_current, room_id=False, device_id=False, user=False):
    #
    html = ''
    #
    try:
        channo = channel[res]['devicekeys'][get_cfg_device_type(room_id, device_id)]
    except:
        channo = False
    #
    # If current channel, create element class text for highlighting
    if bool(chan_current) and channo == chan_current:
        chan_highlight = 'chan-highlight'
    else:
        chan_highlight = ''
    #
    # Create element id, including user name if required (user name prevents duplication of id names within page)
    chan_id = str(user).lower()+'_' if user else ''
    chan_id += category.replace(' ', '').lower()
    chan_id += channel['name'].replace(' ', '').lower()
    #
    if x > 1 and x % 6 == 0:
        html += '</div><div class="row">'
    #
    html += urlopen('web/html_tvguide/tvguide-grid_item.html').read().encode('utf-8').format(id=('chan' + str(channo)),
                                                                                             chan_id=chan_id,
                                                                                             cls_highlight=chan_highlight,
                                                                                             imgchan=channel[res]['logo'],
                                                                                             channame=channel['name'],
                                                                                             room_id=room_id,
                                                                                             device_id=device_id,
                                                                                             channo=channo)
    #
    return html