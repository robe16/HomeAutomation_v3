class object_raspberrypi:

    def __init__ (self, STRname, STRipaddress):
        self._STRipaddress = STRipaddress
        self._type = "xboxone"
        self._name = STRname
        self._html = "object_raspberrypi.html"
        self._img = "logo_raspberrypi.png"
        self._tvguide = False

    def getName(self):
        return self._name

    def getIP(self):
        return self._STRipaddress

    def getTvguide_use(self):
        return self._tvguide

    def getHtml(self):
        return self._html

    def getLogo(self):
        return self._img