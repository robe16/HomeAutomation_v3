from urllib import urlopen


def _settings_devices():
    # TODO - code to create entire page to reflect json config file
    return urlopen('web/html_settings/settings_devices.html').read().encode('utf-8').format(groups = '',
                                                                                            num = str(0))

def _settings_devices_selection():
    #
    body = '<div class="row">'
    count = 0
    devices = [['LG TV', 'logo_lg.png'],
               ['Virgin Media', 'logo_virgin.png'],
               ['Xbox One', 'logo_xboxone.png'],
               ['Nest Account', 'logo_nest_blue.png']]
    #
    for dvc in devices:
        if count> 0 and count % 4 == 0:
            body += '</div><div class="row">'
        body += urlopen('web/html_settings/settings_devices_selection_item.html').read().encode('utf-8').format(name = dvc[0],
                                                                                                                img = dvc[1])
        count += 1
    #
    body += '</div>'
    #
    return body