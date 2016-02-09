from urllib import urlopen
from web_menu import html_menu
from web_settings_devices import settings_devices, settings_devices_selection
from web_settings_tvguide import settings_tvguide
from list_devices import get_device_logo, get_device_html_settings, get_device_settings_dict


def create_settings_devices(user, arr_devices):
    body = settings_devices(arr_devices)
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title='Settings: Devices') + \
           html_menu(user, arr_devices) + \
           urlopen('web/body.html').read().encode('utf-8').format(body=body) + \
           urlopen('web/message_popup.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


def settings_devices_requests(request):
    #
    if request.query.gethtml == 'selection':
        #
        return settings_devices_selection(request.query.grpnum)
        #
    elif request.query.gethtml == 'group':
        #
        return urlopen('web/html_settings/settings_devices_group.html').read().encode('utf-8').format(group_name='',
                                                                                                      devices='',
                                                                                                      num=str(request.query.num))
        #
    elif request.query.gethtml == 'device':
        #
        html = get_device_html_settings(request.query.device)
        #
        dict = get_device_settings_dict(request.query.device)
        dict['img'] = get_device_logo(request.query.device)
        #
        if html:
            return urlopen('web/html_settings/devices/' + html).read().encode('utf-8').format(**dict)
        else:
            return ''
        #
    #
    return False


def create_settings_tvguide(user, arr_devices):
    body = settings_tvguide()
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title='Settings: TV Guide') + \
           html_menu(user, arr_devices) + \
           urlopen('web/body.html').read().encode('utf-8').format(body=body) + \
           urlopen('web/message_popup.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


# TODO - now part of device settings pages (not dedicated)
# def create_settings_nest(user, arr_devices, clientID, STRnest_pincode, random):
#     nesturl = 'https://home.nest.com/login/oauth2?client_id={}&state={}'.format(clientID, random)
#     pincode = ' value="{}"'.format(STRnest_pincode) if bool(STRnest_pincode) else ''
#     #print STRnest_pincode
#     body = urlopen('web/comp_alert.html').read().encode('utf-8').format(body="-") + \
#            urlopen('web/settings_devices_nest.html').read().encode('utf-8').format(nesturl, pincode)
#     #
#     return urlopen('web/header.html').read().encode('utf-8').format(title='[DEPRECIATED] Settings: Nest Account') +\
#            html_menu(user, arr_devices) +\
#            urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
#            urlopen('web/footer.html').read().encode('utf-8')
