from urllib import urlopen
from web_menu import html_menu
from web_settings_devices import settings_devices, settings_devices_selection, settings_devices_group
from web_settings_tvguide import settings_tvguide
from list_devices import get_device_logo, get_device_html_settings, get_device_settings_dict


def create_settings_devices(user):
    body = settings_devices()
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title='Settings: Devices') + \
           html_menu(user) + \
           urlopen('web/body.html').read().encode('utf-8').format(header='Settings: Devices', body=body) + \
           urlopen('web/message_popup.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')


def settings_devices_requests(request):
    #
    if request.query.gethtml == 'selection':
        #
        return settings_devices_selection(request.query.grpnum, request.query.dvcnum)
        #
    elif request.query.gethtml == 'group':
        #
        return settings_devices_group(request.query.grpnum, 0)
        #
    elif request.query.gethtml == 'device':
        #
        html = get_device_html_settings(request.query.device)
        #
        if html:
            dict = get_device_settings_dict(request.query.device)
            dict['img'] = get_device_logo(request.query.device)
            dict['dvc_ref'] = '{grpnum}_{dvcnum}'.format(grpnum=request.query.grpnum, dvcnum=request.query.dvcnum)
            #
            return urlopen('web/html_settings/devices/' + html).read().encode('utf-8').format(**dict)
        else:
            return ''
        #
    #
    return False


def create_settings_tvguide(user):
    body = settings_tvguide()
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title='Settings: TV Guide') + \
           html_menu(user) + \
           urlopen('web/body.html').read().encode('utf-8').format(header='Settings: TV Guide', body=body) + \
           urlopen('web/message_popup.html').read().encode('utf-8') + \
           urlopen('web/footer.html').read().encode('utf-8')