from pyicloud import PyiCloudService

from bundles.accounts.account import Account
from config.bundles.config_bundles import get_cfg_account_detail, set_cfg_account_detail
from lists.devices.list_devices import get_device_detail, get_device_name, get_device_html_settings
from log.console_messages import print_error, print_msg


class account_icloud(Account):

    def __init__ (self, account_id):
        #
        Account.__init__(self, 'icloud_account', account_id)
        #

    def _dvc_name(self):
        return 'iCloud'

    def _type_name(self):
        return get_device_name(self._type)

    def _username(self):
        return get_cfg_account_detail(self._account_id, 'username')

    def _password(self):
        return get_cfg_account_detail(self._type, 'password')





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
            if not self._tokencheck():
                print_error('Nest command could not be sent - error encountered with retrieving new authorisation code', dvc_or_acc_id=self.dvc_or_acc_id())
                return False
            #
            nest_model = request['nest_model']
            nest_device_id = request['nest_device_id']
            nest_device = request['nest_device']
            value = request['value']
            #
            if nest_device == 'thermostats':
                #
                if command == 'temp':
                    #json_cmd = {'bundles': {'thermostats': {nest_device_id: {'target_temperature_c': value}}}}
                    json_cmd = {'target_temperature_' + self._temp_unit : float(value)}
                    if self._send_nest_json(json_cmd, nest_model, nest_device, nest_device_id):
                        return True
                #
            return False
            #
        except Exception as e:
            print_error('Exception encountered sending ' + command + ' - ' + str(e), dvc_or_acc_id=self.dvc_or_acc_id())
            return False