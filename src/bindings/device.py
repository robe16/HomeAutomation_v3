from config.bindings.config_bindings import get_cfg_group_name, get_cfg_thing_name, get_cfg_thing_detail_private
from lists.bindings.list_bindings import get_binding_detail, get_binding_name, get_binding_logo


class Device:

    def __init__(self, type, group_seq, device_seq):
        self._group_seq = group_seq
        self._device_seq = device_seq
        self._type = type

    def dvc_id(self):
        return get_cfg_group_name(self._group_seq) + ':' + get_cfg_thing_name(self._group_seq, self._device_seq)

    def _ipaddress(self):
        return get_cfg_thing_detail_private(self._group_seq, self._device_seq, 'ipaddress')

    def _port(self):
        return get_binding_detail(self._type, 'port')

    def _logo(self):
        return get_binding_logo(self._type)

    def _dvc_name(self):
        return get_cfg_thing_name(self._group_seq, self._device_seq)

    def _type_name(self):
        return get_binding_name(self._type)

    def sendCmd(self, request):
        # Mastered in each of the device specific classes
        pass

    def getData(self, request):
        # Mastered in each of the device specific classes
        pass
