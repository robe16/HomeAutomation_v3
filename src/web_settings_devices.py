from urllib import urlopen


def _settings_devices():
    # TODO - code to create entire page to reflect json config file
    return urlopen('web/html_settings/settings_devices.html').read().encode('utf-8').format(groups = '',
                                                                                            num = str(0))

def _settings_devices_selection():
    #
    body = ''
    count = 0
    devices = [['LG TV', 'logo_lg.png'],
               ['Virgin Media', 'logo_virgin.png'],
               ['Xbox One', 'logo_xboxone.png'],
               ['Nest Account', 'logo_nest_blue.png'],
               ['Test 1', 'logo_other.png'],
               ['Test 2', 'logo_other.png'],
               ['Test 3', 'logo_other.png'],
               ['Test 4', 'logo_other.png'],
               ['Test 5', 'logo_other.png'],
               ['Test 6', 'logo_other.png']]
    #
    for dvc in devices:
        if count % 4 == 0:
            body += '<br>'
        body += urlopen('web/html_settings/devices/settings_devices_selection_item.html').read().encode('utf-8').format(name = dvc[0],
                                                                                                                        img = dvc[1])
        count += 1
    #
    return body