from urllib import urlopen
from console_messages import print_error
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
        print_error('Attempting to create HTML for {grp} - {dvc}: {err}'.format(grp=group_name, dvc=device_name, err=e))
        #
        html_body += urlopen('web/comp_alert.html').read().encode('utf-8').format(type='alert-danger',
                                                                                  visible='visible',
                                                                                  body='<strong>An error has occurred!!</strong> Please try again and if the issue persists check the server setup.')
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