class object_raspberrypi:

    def __init__ (self, STRname, STRsource):
        self._type = "xboxone"
        self._name = STRname
        self._html = "object_raspberrypi.html"
        self._img = "logo_raspberrypi.png"
        self._tvguide = False
        self._source = STRsource

    def getName(self):
        return self._name

    def getTvguide_use(self):
        return self._tvguide

    def getHtml(self):
        return self._html

    def getSource(self):
        return self._source

    def getLogo(self):
        return self._img