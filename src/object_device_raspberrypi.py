from urllib import urlopen
from list_devices import get_device_logo, get_device_html_command, get_device_html_settings

class object_raspberrypi:

    def __init__ (self, label, ipaddress):
        self._type = "raspberrypi"
        self._label = label
        self._ipaddress = ipaddress
        self._tvguide = False

    def getLabel(self):
        return self._label

    def getType(self):
        return self._type

    def getIP(self):
        return self._ipaddress

    def getTvguide_use(self):
        return self._tvguide

    def getLogo(self):
        return get_device_logo(self._type)

    def getHtml(self, group_name):
        device_url = 'device/{group}/{device}'.format(group=group_name, device=self._label.lower().replace(' ',''))
        html = get_device_html_command(self._type)
        return urlopen('web/html_devices/' + html).read().encode('utf-8').format(url=device_url)