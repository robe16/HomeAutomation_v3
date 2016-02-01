from urllib import urlopen


def _settings_devices():
    #
    return urlopen('web/html_settings/settings_devices.html').read().encode('utf-8').format(groups='')