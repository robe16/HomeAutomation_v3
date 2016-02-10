from urllib import urlopen
from list_devices import get_device_logo, get_device_html_command, get_device_html_settings

class object_nest_account:

    def __init__ (self, token, tokenexpiry, pincode):
        self._type = 'nest_account'
        self._label = 'Nest'
        self._token = token
        self._tokenexpiry = tokenexpiry
        self._pincode = pincode
        self._tvguide = False

    def getLabel(self):
        return self._label

    def getType(self):
        return self._type

    def getLogo(self):
        return get_device_logo(self._type)

    def getTvguide_use(self):
        return self._tvguide

    def getHtml(self, group_name):
        html = get_device_html_command(self._type)
        return urlopen('web/html_devices/' + html).read().encode('utf-8')

    def getHtml_settings(self):
        html = get_device_html_settings(self._type)
        return urlopen('web/html_settings/devices/' + html).read().encode('utf-8').format(img = self.getLogo(),
                                                                                          name = self._label,
                                                                                          pincode = self._pincode,
                                                                                          token = self._token,
                                                                                          tokenexpiry = self._tokenexpiry)


    def getToken(self):
        return self._token

    def getTokenexpiry(self):
        return self._tokenexpiry

    def setToken(self, token):
        self._token = token

    def setTokenexpiry(self, tokenexpiry):
        self._tokenexpiry = tokenexpiry

    def setPincode(self, pincode):
        self._pincode = pincode