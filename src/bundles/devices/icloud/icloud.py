from pyicloud import PyiCloudService

from bundles.devices.device import Device
from config.bundles.config_bundles import get_cfg_device_detail
from lists.devices.list_devices import get_device_detail, get_device_name, get_device_html_settings
from log.console_messages import print_error, print_msg


class account_icloud(Device):

    def __init__ (self, group_id, device_id):
        #
        Device.__init__(self, 'icloud_account', group_id, device_id)
        #

    def _dvc_name(self):
        return 'iCloud'

    def _type_name(self):
        return get_device_name(self._type)

    def _username(self):
        return get_cfg_device_detail(self._group_id, self._device_id, 'username')

    def _password(self):
        return get_cfg_device_detail(self._group_id, self._device_id, 'password')





    #TODO
    def getData(self, request):
        #
        try:
            #
            if request['data'] == 'data':
                return self._read_nest_json()
            else:
                return False
            #
        except Exception as e:
            print_error('Failed to return requested data {request} - {error}'.format(request=request['data'],
                                                                                     error=e))
            return False

    # TODO
    def sendCmd(self, request):
        #
        command = request['command']
        #
        try:
            #
            return False
            #
        except Exception as e:
            print_error('Exception encountered sending ' + command + ' - ' + str(e), dvc_id=self.dvc_id())
            return False