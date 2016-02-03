from urllib import urlopen


def _settings_devices():
    # TODO - code to create entire page to reflect json config file
    return urlopen('web/html_settings/settings_devices.html').read().encode('utf-8').format(groups = '',
                                                                                            num = str(0))