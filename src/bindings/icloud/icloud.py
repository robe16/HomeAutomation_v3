from pyicloud import PyiCloudService

from bindings.device import Device
from config.bindings.config_bindings import get_cfg_device_detail
from lists.bindings.list_bindings import get_binding_detail, get_binding_name, get_binding_html_settings
from log.console_messages import print_error, print_msg


class account_icloud(Device):

    def __init__ (self, group_id, device_id):
        #
        Device.__init__(self, 'icloud_account', group_id, device_id)
        #

    def _dvc_name(self):
        return 'iCloud'

    def _type_name(self):
        return get_binding_name(self._type)

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