import datetime
import json
import requests as requests

from bindings.device import Device
from config.bindings.config_bindings import get_cfg_thing_detail_private, set_cfg_thing_detail
from lists.bindings.list_bindings import get_binding_detail, get_binding_name, get_binding_html_settings
from log.console_messages import print_error, print_msg
from auth import get_accesstoken
from cfg import date_format

# Nest API Documentation: https://developer.nest.com/documentation/api-reference

class account_nest(Device):

    nestSession = requests.Session()

    nesturl_api = 'https://developer-api.nest.com/'
    #
    _temp_unit = 'c'

    def __init__ (self, group_seq, device_seq):
        #
        Device.__init__(self, 'nest_account', group_seq, device_seq)
        #
        self._tokencheck()
        self.createSession()

    def createSession(self):
        with requests.Session() as s:
            s.headers.update({'Authorization': self._header_token(),
                              'Connection': 'close',
                              'content-type': 'application/json'})
        self.nestSession = s

    def _dvc_name(self):
        return 'Nest'
        #return get_device_config_detail(self._grp_num, self._dvc_num, "name")

    def _type_name(self):
        return get_binding_name(self._type)

    def _state(self):
        return get_cfg_thing_detail_private(self._group_seq, self._device_seq, 'state')

    def _token(self):
        return get_cfg_thing_detail_private(self._group_seq, self._device_seq, 'token')

    def _set_token(self, token):
        return set_cfg_thing_detail(self._group_seq, self._device_seq, 'token', token)

    def _tokenexpiry(self):
        return get_cfg_thing_detail_private(self._group_seq, self._device_seq, 'tokenexpiry')

    def _set_tokenexpiry(self, tokenexpiry):
        return set_cfg_thing_detail(self._group_seq, self._device_seq, 'tokenexpiry', tokenexpiry)

    def _pincode(self):
        return get_cfg_thing_detail_private(self._group_seq, self._device_seq, 'pincode')

    def _redirect_url(self):
        return get_cfg_thing_detail_private(self._group_seq, self._device_seq, 'redirect_url')

    def _set_redirect_url(self, redirect_url):
        return set_cfg_thing_detail(self._group_seq, self._device_seq, 'redirect_url', redirect_url)

    def _clientid(self):
        return get_binding_detail(self._type, 'client_id')

    def _clientsecret(self):
        return get_binding_detail(self._type, 'client_secret')

    def getData(self, request):
        #
        try:
            #
            if request['data'] == 'data':
                nest_data = self._read_json_all()
                nest_data.pop('metadata')
                return nest_data
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
                print_error('Nest command could not be sent - error encountered with retrieving new authorisation code', dvc_id=self.dvc_id())
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
                    json_cmd = {'target_temperature_' + self._temp_unit : float(value)}
                    if self._send_nest_json(json_cmd, nest_model, nest_device, nest_device_id):
                        return True
                #
            return False
            #
        except Exception as e:
            print_error('Exception encountered sending ' + command + ' - ' + str(e), dvc_id=self.dvc_id())
            return False

    def _tokencheck(self):
        print_msg('Checking Auth Token', dvc_id=self.dvc_id())
        if self._checkToken():
            return True
        else:
            return self._getNewToken()

    def _checkToken(self):
        return datetime.datetime.now() < datetime.datetime.strptime(self._tokenexpiry(), date_format) if bool(self._tokenexpiry()) else False

    def _getNewToken(self):
        #
        try:
            #
            token_response = get_accesstoken(self._clientid(),
                                             self._clientsecret(),
                                             self._pincode())
            #
            print_msg('Success retrieving new Access Token', dvc_id=self.dvc_id())
            #
            self._set_token(token_response['token'])
            self._set_tokenexpiry(token_response['tokenexpiry'])
            #
            return True
            #
        except:
            return False

    def _read_json_all(self):
        return self._read_nest_json()

    def _read_json_metadata(self):
        return self._read_nest_json(model='metadata')

    def _read_json_devices(self, device=False, device_id=False):
        if bool(device) and bool(device_id):
            device_url = '{device}/{device_id}'.format(device=device, device_id=device_id)
        else:
            device_url = ''
        return self._read_nest_json(model='bindings'+device_url)

    def _read_json_structures(self):
        return self._read_nest_json(model='structures')

    def _read_nest_json(self, model=''):
        #
        r = self.nestSession.get(self._get_url() + model)
        #
        if len(r.history) > 0:
            if r.history[0].is_redirect:
                self._set_redirect_url(r.url)
        #
        if str(r.status_code).startswith('4'):
            return False
        #
        return r.json()

    def _send_nest_json (self, json_cmd, model, device, id, retry=0):
        #
        if retry >= 2:
            return False
        #
        url2 = '{model}/{device}/{id}'.format(model=model, device=device, id=id)
        #
        r = self.nestSession.put(self._get_url() + url2,
                         data=json.dumps(json_cmd))
        #
        if len(r.history) > 0:
            if r.history[0].is_redirect:
                self._set_redirect_url(r.url)
        #
        if str(r.status_code).startswith('4'):
            return False
        #
        return r.json()

    def _get_url(self):
        #
        if self._redirect_url() != '':
            return self._redirect_url()
        else:
            return self.nesturl_api

    def _header_token(self):
        return 'Bearer {authcode}'.format(authcode=self._token())