from urllib import urlopen
from web_tvlistings import html_listings_user_and_all


def _create_device_page(user, tvlistings, device, group_name, device_name):
    #
    if not device:
        return ''
    #
    html_body = ''
    try:
        html_body = device.getHtml(listings=tvlistings, user=user)
    except Exception as e:
        print e
    return html_body


def refresh_tvguide(tvlistings, device=None, group_name=False, device_name=False, user=False):
    # Attempt getting current channel from device
    try:
        chan_current = device.getChan()
    except:
        chan_current = False
    #
    return True
    #return html_listings_user_and_all(tvlistings, group_name=group_name, device_name=device_name, chan_current=chan_current, user=user)