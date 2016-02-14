from urllib import urlopen
from datetime import datetime
import string
import random
import json
from send_cmds import sendHTTP
from config_devices import get_device_json, write_config_devices
from list_devices import get_device_logo, get_device_html_command, get_device_html_settings, get_device_detail

class object_nest_account:

    def __init__ (self, group, token, tokenexpiry, pincode, state):
        self._type = 'nest_account'
        self._label = 'Nest'
        self._group = group
        self._token = token
        self._tokenexpiry = tokenexpiry.strptime("%d %m %Y %H:%M:%S") if bool(tokenexpiry) else False
        if self._checkToken():
            self._getNewToken()
        self._pincode = pincode
        self._state = state
        self._tvguide = False

    def getLabel(self):
        return self._label

    def getType(self):
        return self._type

    def getLogo(self):
        return get_device_logo(self._type)

    def getTvguide_use(self):
        return self._tvguide

    def getHtml(self):
        html = get_device_html_command(self._type)
        return urlopen('web/html_devices/' + html).read().encode('utf-8')

    def getHtml_settings(self, dvc_num):
        html = get_device_html_settings(self._type)
        randomstring = (random.choice(string.ascii_lowercase) for i in range(5))
        if html:
            return urlopen('web/html_settings/devices/' + html).read().encode('utf-8').format(img = self.getLogo(),
                                                                                              name = self._label,
                                                                                              pincode = self._pincode,
                                                                                              clientid = get_device_detail(self._type, 'client_id'),
                                                                                              state = randomstring,
                                                                                              token = self._token,
                                                                                              tokenexpiry = self._tokenexpiry.strftime("%d %m %Y %H:%M:%S"),
                                                                                              dvc_ref='{grpnum}_{dvcnum}'.format(grpnum=self._group, dvcnum=dvc_num))
        else:
            return ''

    def _checkToken(self):
        return datetime.now() < self._tokenexpiry if bool(self._tokenexpiry) else False

    def _getNewToken(self):
        url = 'https://api.home.nest.com/oauth2/access_token?'+\
              'client_id={clientid}&'+\
              'code={authcode}&'+\
              'client_secret={clientsecret}&g'+\
              'rant_type=authorization_code'.format(clientid=get_device_detail(self._type, 'client_id'),
                                                    authcode=self._pincode,
                                                    clientsecret=get_device_detail(self._type, 'client_secret'))
        response = sendHTTP(url, 'close')
        if response:
            data = json.load(response.read())
            #
            self._token = data['access_token']
            self._tokenexpiry = datetime.now() + datetime.timedelta(milliseconds=data['expires_in'])
            #
            self._updateConfig()
            #
            return True
        else:
            return False

    def _updateConfig(self):
        data = get_device_json()
        #
        grpX = 0
        for data_group in data:
            if data_group['group'] == self._group:
                dvcX = 0
                for data_dvc in data_group['devices']:
                    if data_dvc['device'] == self._type:
                        data[grpX]['devices'][dvcX]['details']['token'] = self._token
                        data[grpX]['devices'][dvcX]['details']['tokenexpiry'] = self._tokenexpiry.strftime("%d %m %Y %H:%M:%S")
                        data[grpX]['devices'][dvcX]['details']['pincode'] = self._pincode
                        data[grpX]['devices'][dvcX]['details']['state'] = self._state
                        write_config_devices(data)
                        return
                    dvcX += 1
            grpX += 1
        #
        return