from src.lists.devices.list_devices import get_device_name, get_device_logo


class InfoService:

    def __init__(self, type):
        self._active = True
        self._type = type

    def _logo(self):
        return get_device_logo(self._type)

    def _type_name(self):
        return get_device_name(self._type)

    def getData(self, request):
        # Mastered in each of the infoservice specific classes
        pass

    def sendCmd(self, request):
        # Mastered in each of the infoservice specific classes
        pass
