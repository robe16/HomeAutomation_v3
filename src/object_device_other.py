from urllib import urlopen

class object_other:

    def __init__ (self, STRname, STRipaddress):
        self._STRipaddress = STRipaddress
        self._type = "other"
        self._name = STRname
        self._img = "logo_other.png"
        self._tvguide = False

    def getName(self):
        return self._name

    def getIP(self):
        return self._STRipaddress

    def getTvguide_use(self):
        return self._tvguide

    def getLogo(self):
        return self._img

    def getHtml(self, group_name):
        device_url = 'device/{group}/{device}'.format(group=group_name, device=self._name.lower().replace(' ',''))
        return urlopen('web/{page}'.format(page="object_other.html")).read().encode('utf-8').format(url=device_url)