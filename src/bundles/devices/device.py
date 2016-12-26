from config.bundles.config_bundles import get_cfg_device_detail
from lists.devices.list_devices import get_device_detail, get_device_name, get_device_logo


class Device:

    def __init__(self, type, room_id, device_id):
        self._room_id = room_id
        self._device_id = device_id
        self._type = type

    def dvc_or_acc_id(self):
        return self._room_id + ':' + self._device_id

    def dvc_or_acc_ref(self):
        return self._room_id + '_' + self._device_id

    def _ipaddress(self):
        return get_cfg_device_detail(self._room_id, self._device_id, 'ipaddress')

    def _port(self):
        return get_device_detail(self._type, 'port')

    def _logo(self):
        return get_device_logo(self._type)

    def _dvc_name(self):
        return get_cfg_device_detail(self._room_id, self._device_id, 'name')

    def _type_name(self):
        return get_device_name(self._type)

    def sendCmd(self, request):
        # Mastered in each of the device specific classes
        pass

    def getData(self, request):
        # Mastered in each of the device specific classes
        pass
