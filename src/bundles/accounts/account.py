from config.bundles.config_bundles import get_cfg_account_detail
from lists.devices.list_devices import get_device_name, get_device_logo


class Account:

    def __init__(self, type, account_id):
        self._account_id = account_id
        self._type = type

    def dvc_or_acc_id(self):
        return self._account_id

    def dvc_or_acc_ref(self):
        return self._account_id

    def _logo(self):
        return get_device_logo(self._type)

    def _dvc_name(self):
        return get_cfg_account_detail(self._account_id, 'name')

    def _type_name(self):
        return get_device_name(self._type)

    def sendCmd(self, request):
        # Mastered in each of the device specific classes
        pass

    def getData(self, request):
        # Mastered in each of the device specific classes
        pass
