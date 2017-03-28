class InfoService:

    def __init__(self, type, group_seq, device_seq):
        self._group_seq = group_seq
        self._device_seq = device_seq
        self._type = type

    def getData(self, request):
        # Mastered in each of the infoservice specific classes
        pass