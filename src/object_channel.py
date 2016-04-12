class object_channel:

    def __init__ (self, name, category, logo, type, devicekeys, listingsrc, listings, listingstimestamp):
        self._name = name
        self._category = category
        self._logo = logo
        self._type = type
        self._devicekeys = devicekeys
        self._listingsrc = listingsrc
        self._listings = listings
        self._listingstimestamp = listingstimestamp

    def name(self):
        return self._name

    def type(self):
        return self._type

    def category(self):
        return self._category

    def logo(self, res=False):
        if not res:
            if self._logo['hd']:
                return self._logo['hd']
            else:
                return self._logo['sd']
        #
        return self._logo[res]

    def devicekeys(self, res, key):
        return self._devicekeys[res][key]

    def listingsrc(self, key):
        return self._listingsrc[key]

    def getListings(self):
        return self._listings

    def putListings(self, listings):
        self._listings = listings

    def listingstimestamp(self):
        return self._listingstimestamp