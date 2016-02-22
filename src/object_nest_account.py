from urllib import urlopen
import datetime
import string
import random
import os
import json
from send_cmds import sendHTTP
from console_messages import print_command, print_error
from list_devices import get_device_logo, get_device_html_command, get_device_html_settings, get_device_detail, get_device_name, set_device_detail

# Nest API Documentation: https://developer.nest.com/documentation/api-reference

class object_nest_account:

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
        #
        html = get_device_html_command(self._type)
        body = self._htmlbody()
        #
        return urlopen('web/html_devices/' + html).read().encode('utf-8').format(group = self._group.lower().replace(' ',''),
                                                                                 device = self._label.lower().replace(' ',''),
                                                                                 body=body)

    def _htmlbody(self):
        #
        devices_html = '<div class="row">'
        #
        try:
            json_devices = self._read_json_devices()
            #
            if not json_devices:
                print_error('Nest devices could not retrieved from Nest server')
                return False
            #
            #
            try:
                therm_ids = json_devices['thermostats'].keys()
            except:
                therm_ids = False
            #
            if bool(therm_ids):
                count = 0
                for therm in therm_ids:
                    if count> 0 and count % 4 == 0:
                        devices_html += '</div><div class="row">'
                    #
                    colwidth = '3'
                    rem = len(therm_ids) - count
                    if rem == 1:
                        colwidth = '12'
                    elif rem == 2:
                        colwidth = '6'
                    elif rem == 3:
                        colwidth = '4'
                    #
                    nest_device_id = json_devices['thermostats'][therm]['device_id']
                    therm_name = json_devices['thermostats'][therm]['name']
                    #
                    if json_devices['thermostats'][therm]['is_online']:
                        #
                        therm_hvac_state = json_devices['thermostats'][therm]['hvac_state']
                        if therm_hvac_state == 'heating':
                            temp_hvac_statement = 'Heating to'
                        elif therm_hvac_state =='cooling':
                            temp_hvac_statement = 'Cooling to'
                        else:
                            temp_hvac_statement = 'Heat set to'
                        #
                        temp_unit_html = '&#8451;' if self._temp_unit == 'c' else '&#8457'
                        therm_temp_target = json_devices['thermostats'][therm]['target_temperature_{unit}'.format(unit=self._temp_unit)]
                        therm_temp_ambient = json_devices['thermostats'][therm]['ambient_temperature_{unit}'.format(unit=self._temp_unit)]
                        #
                    else:
                        #
                        therm_hvac_state = 'offline'
                        temp_hvac_statement = 'Offline'
                        temp_unit_html = ''
                        therm_temp_target = ''
                        therm_temp_ambient = ''
                        #
                    #
                    devices_html += urlopen('web/html_devices/object_nest_account_thermostat.html')\
                        .read().encode('utf-8').format(colwidth=colwidth,
                                                       group=self._group.lower().replace(' ',''),
                                                       device=self._label.lower().replace(' ',''),
                                                       nest_device_id=nest_device_id,
                                                       name=therm_name,
                                                       temp_hvac=temp_hvac_statement,
                                                       temp_target=therm_temp_target,
                                                       temp_ambient=therm_temp_ambient,
                                                       temp_unit=temp_unit_html,
                                                       hvac=therm_hvac_state,
                                                       new_temp_up=therm_temp_target+0.5,
                                                       new_temp_down=therm_temp_target-0.5)
                    #
                    count += 1
                    #
            #
            #
            try:
                smoke_ids = json_devices['smoke_co_alarms'].keys()
            except:
                smoke_ids = False
            #
            if bool(smoke_ids):
                count = 0
                for smoke in smoke_ids:
                    if count> 0 and count % 4 == 0:
                        devices_html += '</div><div class="row">'
                    #
                    colwidth = '3'
                    rem = len(smoke_ids) - count
                    if rem == 1:
                        colwidth = '12'
                    elif rem == 2:
                        colwidth = '6'
                    elif rem == 3:
                        colwidth = '4'
                    #
                    nest_device_id = json_devices['smoke_co_alarms'][smoke]['device_id']
                    smoke_name = json_devices['smoke_co_alarms'][smoke]['name']
                    #
                    if json_devices['smoke_co_alarms'][smoke]['is_online']:
                        #
                        smoke_online = 'online'
                        #
                        battery_health = json_devices['smoke_co_alarms'][smoke]['battery_health']
                        # ok
                        # replace
                        #
                        co_alarm_state = json_devices['smoke_co_alarms'][smoke]['co_alarm_state']
                        # ok
                        # warning
                        # emergency
                        #
                        smoke_alarm_state = json_devices['smoke_co_alarms'][smoke]['smoke_alarm_state']
                        # ok
                        # warning
                        # emergency
                        #
                        ui_color_state = json_devices['smoke_co_alarms'][smoke]['ui_color_state']
                        # gray
                        # green
                        # yellow
                        # red
                        #
                    else:
                        #
                        smoke_online = 'offline'
                        battery_health = ''
                        co_alarm_state = ''
                        smoke_alarm_state = ''
                        #
                    #
                    devices_html += urlopen('web/html_devices/object_nest_account_smoke_co_alarm.html')\
                        .read().encode('utf-8').format(colwidth=colwidth,
                                                       group=self._group.lower().replace(' ',''),
                                                       device=self._label.lower().replace(' ',''),
                                                       nest_device_id=nest_device_id,
                                                       name=smoke_name,
                                                       online=smoke_online,
                                                       battery_health=battery_health,
                                                       co_alarm_state=co_alarm_state,
                                                       smoke_alarm_state=smoke_alarm_state)
                    #
                    count += 1
                    #
            #
            #
            try:
                cam_ids = json_devices['cameras'].keys()
            except:
                cam_ids = False
            #
            #
        except Exception as e:
            devices_html = '<div id="body" class="row">ERROR</div>'
            print_error('Nest devices could not be compiled into html - ' + str(e))
        #
        devices_html += '</div>'
        return devices_html

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
            if not self._tokencheck():
                print_error('Nest command could not be sent - error encountered with retrieving new authorisation code')
                return False
            #
            nest_model = request.query.nest_model or False
            nest_device_id = request.query.nest_device_id or False
            nest_device = request.query.nest_device or False
            value = request.query.value or False
            #
            if nest_device == 'thermostats':
                #
                if command == 'temp':
                    #json_cmd = {'devices': {'thermostats': {nest_device_id: {'target_temperature_c': value}}}}
                    json_cmd = {'target_temperature_' + self._temp_unit : float(value)}
                    if self._send_nest_json(json_cmd, nest_model, nest_device, nest_device_id):
                        return self._htmlbody()
                #
            return False
            #
        except Exception as e:
            print_command(command, get_device_name(self._type), '', 'ERROR: Exception encountered - ' + str(e))
            return False

    def _tokencheck(self):
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
        url = (self.nesturl_tokenexchange).format(authcode=self._pincode,
                                                  clientid=get_device_detail(self._type, 'client_id'),
                                                  clientsecret=get_device_detail(self._type, 'client_secret'))
        #
        response = sendHTTP(url, 'close', method='POST')
        #
        if isinstance(response, bool):
            print_error('Nest auth code not received by Nest server')
            return False
        #
        try:
            response = response.read()
        except Exception as e:
            print_error('Nest auth code not received by Nest server - ' + str(e))
            return False
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

    def _read_json_all(self):
        return self._read_nest_json()

    def _read_json_metadata(self):
        return self._read_nest_json(model='/metadata')

    def _read_json_devices(self, device=False, device_id=False):
        if bool(device) and bool(device_id):
            device_url = '/{device}/{device_id}'.format(device=device, device_id=device_id, redirect_type=self._type)
        else:
            device_url = ''
        return self._read_nest_json(model='/devices'+device_url)

    def _read_json_structures(self):
        return self._read_nest_json(model='/structures')

    def _read_nest_json(self, model=''):
        #
        response = sendHTTP(self.nesturl_api, 'close', url2=model, header_auth=self._header_token(), redirect_type=self._type)
        #
        return json.load(response)

    def _send_nest_json (self, json_cmd, model, device, id, retry=0):
        #
        if retry >= 2:
            return False
        #
        url2 = '/{model}/{device}/{id}'.format(model=model, device=device, id=id)
        #
        response = sendHTTP(self._get_url(), 'close', url2=url2, method='PUT', header_auth=self._header_token(), data=json.dumps(json_cmd), contenttype='application/json', redirect_type=self._type)
        #
        if not response and not get_device_detail(self._type, 'redirect_url') == '':
            # if the command failed and there is redirect url, attempt without the url
            retry += 1
            set_device_detail(self._type, 'redirect_url', '')
            return self._send_nest_json (json_cmd, model, device, id, retry=retry)
        else:
            return response
        #

    def _get_url(self):
        #
        if get_device_detail(self._type, 'redirect_url') != '':
            return get_device_detail(self._type, 'redirect_url')
        else:
            return self.nesturl_api

    def _header_token(self):
        return 'Bearer {authcode}'.format(authcode=self._token)