class object_other:

    def __init__ (self, STRname, STRsource):
        self._type = "other"
        self._name = STRname
        self._html = "object_other.html"
        self._img = "logo_other.png"
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