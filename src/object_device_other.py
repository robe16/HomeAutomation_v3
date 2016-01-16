class object_other:

    def __init__ (self, STRname, STRipaddress):
        self._STRipaddress = STRipaddress
        self._type = "other"
        self._name = STRname
        self._html = "object_other.html"
        self._img = "logo_other.png"
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