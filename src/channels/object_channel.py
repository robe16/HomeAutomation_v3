from src.lists.channels.list_channels import \
    get_channel_item_type, \
    get_channel_item_res_devicekey,\
    get_channel_item_res_freeview,\
    get_channel_item_res_logo,\
    get_channel_item_res_package

class object_channel:

    def __init__ (self, name, category, listingsrc, listings, listingstimestamp):
        self._name = name
        self._category = category
        self._listingsrc = listingsrc
        self._listings = listings
        self._listingstimestamp = listingstimestamp

    def category(self):
        return self._category

    def name(self):
        return self._name

    def type(self):
        return get_channel_item_type(self._category, self._name)

    def logo(self, res):
        return get_channel_item_res_logo(self._category, self._name, res)

    def devicekeys(self, res, device_type):
        return get_channel_item_res_devicekey(self._category, self._name, res, device_type)

    def freeview(self, res):
        return get_channel_item_res_freeview(self._category, self._name, res)

    def package(self, res, package_name):
        return get_channel_item_res_package(self._category, self._name, res, package_name)

    def listingsrc(self, key):
        return self._listingsrc[key]

    def getListings(self):
        return self._listings

    def putListings(self, listings):
        self._listings = listings

    def listingstimestamp(self):
        return self._listingstimestamp