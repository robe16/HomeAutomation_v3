import datetime
import json
import random
import string
from urllib import urlopen

import requests as requests

from src.bundles.accounts.account import Account
from src.config.bundles.config_bundles import get_cfg_account_detail, set_cfg_account_detail
from src.lists.devices.list_devices import get_device_detail, get_device_name, get_device_html_settings
from src.log.console_messages import print_error, print_msg


# Nest API Documentation: https://developer.nest.com/documentation/api-reference

class account_nest(Account):

    # Static variable used as part of using Nest's APIs
    nesturl_api = 'https://developer-api.nest.com'
    nesturl_tokenexchange = ('https://api.home.nest.com/oauth2/access_token?' +
                             'code={authcode}&' +
                             'client_id={clientid}&' +
                             'client_secret={clientsecret}&' +
                             'grant_type=authorization_code')
    #
    _dateformat = '%d/%m/%Y %H:%M:%S'
    _temp_unit = 'c'

    def __init__ (self, account_id):
        #
        Account.__init__(self, 'nest_account', account_id)
        #
        self._token = ''
        self._tokenexpiry = ''
        self._pincode = ''
        self._state = ''
        self._getConfig()
        #
        self._tokencheck()
        #
        self._redirect_url = ''

    def _dvc_name(self):
        return 'Nest'
        #return get_device_config_detail(self._grp_num, self._dvc_num, "name")

    def _type_name(self):
        return get_device_name(self._type)

    def _pincode(self):
        return get_cfg_account_detail(self._account_id, 'pincode')

    def _clientid(self):
        return get_device_detail(self._type, 'client_id')

    def _clientsecret(self):
        return get_device_detail(self._type, 'client_secret')

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

    def _tokencheck(self):
        print_msg('Checking Auth Token', dvc_or_acc_id=self.dvc_or_acc_id())
        if bool(self._pincode):
            if self._checkToken():
                return True
            else:
                return self._getNewToken()
        else:
            return False

    def _checkToken(self):
        return datetime.datetime.now() < self._tokenexpiry if bool(self._tokenexpiry) else False

    def _getNewToken(self):
        #
        url = 'https://api.home.nest.com/oauth2/access_token?code={PIN_CODE}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=authorization_code'.format(PIN_CODE=self._pincode,
                                                                                                                                                                       CLIENT_ID=self._clientid(),
                                                                                                                                                                       CLIENT_SECRET=self._clientsecret())
        #
        headers = {'Connection': 'close',
                   'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8'}
        #
        r = requests.post(url,
                          headers=headers)
        #
        if r.status_code != requests.codes.ok:
            print_error('Auth code not received by Nest server', dvc_or_acc_id=self.dvc_or_acc_id())
            return False
        #
        try:
            response = r.content
        except Exception as e:
            print_error('Auth code not received by Nest server - ' + str(e), dvc_or_acc_id=self.dvc_or_acc_id())
            return False
        #
        if response:
            try:
                data = json.loads(response)
            except Exception as e:
                print_error('Auth code not processed into json object - ' + str(e), dvc_or_acc_id=self.dvc_or_acc_id())
                return False
            #
            exp = datetime.datetime.now() + datetime.timedelta(milliseconds=data['expires_in'])
            #
            set_cfg_account_detail(self._account_id, 'token', data['access_token'])
            set_cfg_account_detail(self._account_id, 'tokenexpiry', exp.strftime(self._dateformat))
            #
            self._token = data['access_token']
            self._tokenexpiry = exp
            #
            print_msg('Success retrieving new Access Token', dvc_or_acc_id=self.dvc_or_acc_id())
            #
            return True
        else:
            return False

    def _getConfig(self):
        self._token = get_cfg_account_detail(self._account_id, "token")
        self._pincode = get_cfg_account_detail(self._account_id, "pincode")
        self._state = get_cfg_account_detail(self._account_id, "state")
        #
        token_exp = get_cfg_account_detail(self._account_id, "tokenexpiry")
        if bool(token_exp):
            self._tokenexpiry = datetime.datetime.strptime(token_exp, self._dateformat)
        else:
            self._tokenexpiry = False

    def _read_json_all(self):
        return self._read_nest_json()

    def _read_json_metadata(self):
        return self._read_nest_json(model='/metadata')

    def _read_json_devices(self, device=False, device_id=False):
        if bool(device) and bool(device_id):
            device_url = '/{device}/{device_id}'.format(device=device, device_id=device_id)
        else:
            device_url = ''
        return self._read_nest_json(model='/bundles'+device_url)

    def _read_json_structures(self):
        return self._read_nest_json(model='/structures')

    def _read_nest_json(self, model=''):
        #
        headers = {'Authorization': self._header_token(),
                   'Connection': 'close',
                   'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8'}
        #
        r = requests.put(self._get_url() + model,
                         data='',
                         headers=headers)
        #
        if str(r.status_code).startswith('4'):
            return False
        elif str(r.status_code).startswith('3'):
            self._redirect_url = r.url
        #
        return json.load(r.content)

    def _send_nest_json (self, json_cmd, model, device, id, retry=0):
        #
        if retry >= 2:
            return False
        #
        url2 = '/{model}/{device}/{id}'.format(model=model, device=device, id=id)
        #
        headers = {'Authorization': self._header_token(),
                   'Connection': 'close',
                   'content-type': 'application/json',
                   'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8'}
        #
        r = requests.put(self._get_url() + url2,
                         data=json.dumps(json_cmd),
                         headers=headers)
        #
        if str(r.status_code).startswith('4'):
            return False
        elif str(r.status_code).startswith('3'):
            self._redirect_url = r.url
        #
        return json.load(r.content)

    def _get_url(self):
        #
        if self._redirect_url != '':
            return self._redirect_url
        else:
            return self.nesturl_api

    def _header_token(self):
        return 'Bearer {authcode}'.format(authcode=self._token)