from urllib import urlopen
from list_devices import read_list_devices, get_device_name, get_device_logo


def _settings_devices():
    # TODO - code to create entire page to reflect json config file
    return urlopen('web/html_settings/settings_devices.html').read().encode('utf-8').format(groups = '',
                                                                                            num = str(0))

def _settings_devices_selection(grpnum):
    #
    body = '<div class="row">'
    count = 0
    devices = read_list_devices()
    #
    for dvc in devices:
        if count> 0 and count % 4 == 0:
            body += '</div><div class="row">'
        #
        name = get_device_name(dvc['type'])
        img = get_device_logo(dvc['type'])
        #
        body += urlopen('web/html_settings/settings_devices_selection_item.html').read().encode('utf-8').format(name = name,
                                                                                                                img = img,
                                                                                                                grpnum = grpnum,
                                                                                                                type = dvc['type'].lower().replace(' ',''))
        count += 1
    #
    body += '</div>'
    #
    return body