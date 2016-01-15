class object_channel:

    def __init__ (self, name, logo, type, enabled, devicekeys, listingsrc, listings, listingstimestamp):
        self._name = name
        self._logo = logo
        self._type = type
        self._enabled = enabled
        self._devicekeys = devicekeys
        self._listingsrc = listingsrc
        self._listings = listings
        self._listingstimestamp = listingstimestamp

    def name(self):
        return self._name

    def logo(self):
        return self._logo

    def type(self):
        return self._type

    def getEnabled(self):
        return self._enabled

    def setEnabled(self, enabled):
        self._enabled = enabled
        return

    def devicekeys(self, key):
        return self._devicekeys[key]

    def listingsrc(self, key):
        return self._listingsrc[key]

    def getListings(self):
        return self._listings

    def putListings(self, listings):
        self._listings = listings

    def listingstimestamp(self, key):
        return self._listingstimestamp