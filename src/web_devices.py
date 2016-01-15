from urllib import urlopen
from web_tvlistings import html_listings_user_and_all


def _create_device_page(user, tvlistings, device, group_name, device_name):
    #
    if not device:
        return ''
    #
    device_url = 'device/{group}/{device}'.format(group=group_name, device=device_name)
    html_body = urlopen('web/{page}'.format(page=device.getHtml())).read().encode('utf-8').format(url=device_url)
    # Get whether device requires TV guide displaying on page
    try:
        bool_tvguideuse = device.getTvguide_use()
    except:
        bool_tvguideuse = False
    # Create tv guide html if required
    if bool_tvguideuse:
        #
        html_tv = refresh_tvguide(user, tvlistings, device, group_name, device_name)
        #
        html_body += '<br>'
        html_body += urlopen('web/tvguide.html').read().encode('utf-8').format(listings=html_tv)
    #
    return html_body


def refresh_tvguide(user, tvlistings, device, group_name, device_name):
    #
    device_url = 'device/{group}/{device}'.format(group=group_name, device=device_name)
    # Attempt getting current channel from device
    try:
        chan_current = device.getChan()
    except:
        chan_current = False
    #
    return html_listings_user_and_all(tvlistings, device_url=device_url, device=device, chan_current=chan_current, user=user)

    # from config_devices import create_device_object_array
    # create_device_page("Rob", None, create_device_object_array(), "Lounge TV")
    # print ('done')
