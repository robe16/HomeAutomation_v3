class object_nest_account:

    def __init__ (self, STRname, token, tokenexpiry, pincode):
        self._type = "nest_account"
        self._name = STRname
        self._html = "object_other.html"
        self._img = "logo_nest_blue.png"
        self._tvguide = False
        self._token = token
        self._tokenexpiry = tokenexpiry
        self._pincode = pincode

    def getName(self):
        return self._name

    def getTvguide_use(self):
        return self._tvguide

    def getHtml(self):
        return self._html

    def getLogo(self):
        return self._img


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