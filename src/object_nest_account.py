from urllib import urlopen
import datetime
import string
import random
import os
import json
from send_cmds import sendHTTP
from console_messages import print_command, print_error
from list_devices import get_device_logo, get_device_html_command, get_device_html_settings, get_device_detail, get_device_name

class object_nest_account:

    # Static variable used as part of using Nest's APIs
    nesturl_api = "https://developer-api.nest.com"
    nesturl_tokenexchange = ('https://api.home.nest.com/oauth2/access_token?' +
                             'code={authcode}&' +
                             'client_id={clientid}&' +
                             'client_secret={clientsecret}&' +
                             'grant_type=authorization_code')
    #
    _dateformat = '%d/%m/%Y %H:%M:%S'


    def __init__ (self, group, token, tokenexpiry, pincode, state):
        self._type = 'nest_account'
        self._label = 'Nest'
        self._group = group
        self._token = token
        self._tokenexpiry = datetime.datetime.strptime(tokenexpiry, self._dateformat) if bool(tokenexpiry) else False
        self._pincode = pincode
        self._state = state
        if bool(self._pincode) and not self._checkToken():
            self._getNewToken()
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

    def getHtml_settings(self, grp_num, dvc_num):
        html = get_device_html_settings(self._type)
        randomstring = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
        #
        try:
            tokexp = self._tokenexpiry.strftime(self._dateformat)
        except:
            tokexp = ''
        #
        if html:
            return urlopen('web/html_settings/devices/' + html).read().encode('utf-8').format(img = self.getLogo(),
                                                                                              name = self._label,
                                                                                              pincode = self._pincode,
                                                                                              clientid = get_device_detail(self._type, 'client_id'),
                                                                                              state = randomstring,
                                                                                              token = self._token,
                                                                                              tokenexpiry = tokexp,
                                                                                              dvc_ref='{grpnum}_{dvcnum}'.format(grpnum=grp_num, dvcnum=dvc_num))
        else:
            return ''


    def sendCmd(self, request):
        #
        command = request.query.command
        #
        try:
            #
            # if not self._check_paired():
            #     print_command (command, get_device_name(self._type), self._ipaddress, "ERROR: Device could not be paired")
            #     return False
            #
            # STRxml = ('<?xml version="1.0" encoding="utf-8"?>' +
            #           '<envelope>' +
            #           '<api type="command">' +
            #           '<name>HandleKeyInput</name>' +
            #           '<value>{value}</value>' +
            #           '</api>' +
            #           '</envelope>').format(value = code)
            # response = sendHTTP(self._ipaddress+":"+str(self._port)+str(self.STRtv_PATHcommand), "close", data=STRxml, contenttype='text/xml; charset=utf-8')
            # if bool(response) and not str(response.getcode()).startswith("2"):
            #     if not self._check_paired():
            #         return False
            #     response = sendHTTP(self._ipaddress+":"+str(self._port)+str(self.STRtv_PATHcommand), "close", data=STRxml, contenttype='text/xml; charset=utf-8')
            # #
            # response = str(response.getcode()).startswith("2") if bool(response) else False
            # print_command (code, get_device_name(self._type), self._ipaddress, bool(response))
            # return response
            return True
            #
        except:
            print_command (command, get_device_name(self._type), '', "ERROR: Exception encountered")
            return False


    def _checkToken(self):
        return datetime.datetime.now() < self._tokenexpiry if bool(self._tokenexpiry) else False

    def _getNewToken(self):
        url = (self.nesturl_tokenexchange).format(authcode=self._pincode,
                                                  clientid=get_device_detail(self._type, 'client_id'),
                                                  clientsecret=get_device_detail(self._type, 'client_secret'))
        #
        # Set 'data' to ' ' in order to force method to POST as opposed to GET
        response = sendHTTP(url, 'close', data=' ')
        #
        try:
            response = response.read()
        except Exception as e:
            print_error('Nest auth code not received by Nest server - ' + str(e))
        #
        if response:
            try:
                data = json.loads(response)
            except Exception as e:
                print_error('Nest auth code not processed into json object - ' + str(e))
                return False
            #
            token = data['access_token']
            tokenexpiry = datetime.datetime.now() + datetime.timedelta(milliseconds=data['expires_in'])
            #
            self._token = token
            self._tokenexpiry = tokenexpiry
            #
            self._updateConfig()
            #
            return True
        else:
            return False

    def _updateConfig(self):
        #
        data = json.load(open(os.path.join('config', 'config_devices.json'), 'r'))
        #
        grpX = 0
        for data_group in data:
            if data_group['group'] == self._group:
                dvcX = 0
                for data_dvc in data_group['devices']:
                    if data_dvc['device'] == self._type:
                        data[grpX]['devices'][dvcX]['details']['token'] = self._token
                        data[grpX]['devices'][dvcX]['details']['tokenexpiry'] = self._tokenexpiry.strftime(self._dateformat)
                        data[grpX]['devices'][dvcX]['details']['pincode'] = self._pincode
                        data[grpX]['devices'][dvcX]['details']['state'] = self._state
                        #
                        try:
                            #
                            with open(os.path.join('config', 'config_devices.json'), 'w+') as output_file:
                                output_file.write(json.dumps(data, indent=4, separators=(',', ': ')))
                                output_file.close()
                            #
                            return True
                        except Exception as e:
                            print_error('Nest token and expiry not saved to config - ' + str(e))
                            return False
                        #
                    dvcX += 1
            grpX += 1
        #
        return False