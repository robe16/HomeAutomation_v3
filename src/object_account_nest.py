from urllib import urlopen
import datetime
import string
import random
import os
import json
import time
from send_cmds import sendHTTP
from console_messages import print_command, print_error, print_msg
from config_devices import get_device_config_detail
from list_devices import get_device_detail, get_device_name, get_device_logo, get_device_html_command, get_device_html_settings
from list_devices import set_device_detail
import cfg

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

    def __init__ (self, grp_num, dvc_num, q_dvc, queues):
        self._type = 'nest_account'
        self._grp_num = grp_num
        self._dvc_num = dvc_num
        #
        self._queue = q_dvc
        self._q_response_web = queues[cfg.key_q_response_web_device]
        self._q_response_cmd = queues[cfg.key_q_response_command]
        self._q_tvlistings = queues[cfg.key_q_tvlistings]
        #
        self._active = True
        self.run()


    def run(self):
            time.sleep(5)
            while self._active:
                # Keep in a loop
                '''
                    Use of self._active allows for object to close itself, however may wish
                    to take different approach of terminting the thread the object loop resides in
                '''
                time.sleep(0.1)
                qItem = self._getFromQueue()
                if bool(qItem):
                    if qItem['response_queue'] == 'stop':
                        self._active = False
                    elif qItem['response_queue'] == cfg.key_q_response_web_device:
                        self._q_response_web.put(self.getHtml())
                    elif qItem['response_queue'] == cfg.key_q_response_command:
                        self._q_response_cmd.put(self.sendCmd(qItem['request']))
                    else:
                        # Code to go here to handle other items added to the queue!!
                        True
            print_msg('Thread stopped - Group {grp_num} Device {dvc_num}: {type}'.format(grp_num=self._grp_num,
                                                                                         dvc_num=self._dvc_num,
                                                                                         type=self._type))

    def _getFromQueue(self):
        if not self._queue.empty():
            return self._queue.get(block=True)
        else:
            return False

    def _logo(self):
        return get_device_logo(self._type)

    def _dvc_name(self):
        return 'Nest'
        #return get_device_config_detail(self._grp_num, self._dvc_num, "name")

    def _type_name(self):
        return get_device_name(self._type)

    def _pincode(self):
        return get_device_config_detail(self._grp_num, self._dvc_num, "pincode")

    def _state(self):
        return get_device_config_detail(self._grp_num, self._dvc_num, "state")

    def _token(self):
        return get_device_config_detail(self._grp_num, self._dvc_num, "token")

    def getHtml(self):
        #
        html = get_device_html_command(self._type)
        body = self._htmlbody()
        #
        script = ("\r\n<script>\r\n" +
                  "setTimeout(function () {\r\n" +
                  "updateNest('/web/device/" + str(self._grp_num) + "/" + str(self._dvc_num) + "?body=true');\r\n" +
                  "}, 30000);\r\n" +
                  "</script>\r\n")
        #
        timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        #
        return urlopen('web/html_devices/' + html).read().encode('utf-8').format(group = str(self._grp_num),
                                                                                 device = str(self._dvc_num),
                                                                                 timestamp=timestamp,
                                                                                 script=script,
                                                                                 body_nest=body)

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
            # Thermostats
            #
            html_therm = get_device_detail(self._type, 'html_therm')
            #
            if html_therm:
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
                            is_online = 'online'
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
                            therm_label = 'Current: '
                            #
                            new_temp_up = therm_temp_target + 0.5
                            new_temp_down = therm_temp_target - 0.5
                            #
                            therm_leaf = json_devices['thermostats'][therm]['has_leaf']
                            #
                        else:
                            #
                            is_online = 'offline'
                            therm_hvac_state = 'offline'
                            temp_hvac_statement = ''
                            temp_unit_html = ''
                            therm_label = 'Offline'
                            therm_temp_target = ''
                            therm_temp_ambient = ''
                            therm_leaf = 'false'
                            new_temp_up = ''
                            new_temp_down = ''
                            #
                        #
                        devices_html += urlopen('web/html_devices/{html_therm}'.format(html_therm=html_therm))\
                            .read().encode('utf-8').format(colwidth=colwidth,
                                                           group=str(self._grp_num),
                                                           device=str(self._dvc_num),
                                                           nest_device_id=nest_device_id,
                                                           name=therm_name,
                                                           therm_label=therm_label,
                                                           is_online=is_online,
                                                           temp_hvac=temp_hvac_statement,
                                                           temp_target=therm_temp_target,
                                                           temp_ambient=therm_temp_ambient,
                                                           temp_unit=temp_unit_html,
                                                           has_leaf=str(therm_leaf).lower(),
                                                           hvac=therm_hvac_state,
                                                           new_temp_up=new_temp_up,
                                                           new_temp_down=new_temp_down)
                        #
                        count += 1
                        #
            #
            # Smoke and CO detectors
            #
            html_smoke = get_device_detail(self._type, 'html_smoke')
            #
            if html_smoke:
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
                            # ok / replace
                            #
                            co_alarm_state = json_devices['smoke_co_alarms'][smoke]['co_alarm_state']
                            # ok / warning / emergency
                            #
                            smoke_alarm_state = json_devices['smoke_co_alarms'][smoke]['smoke_alarm_state']
                            # ok / warning / emergency
                            #
                            ui_color_state = json_devices['smoke_co_alarms'][smoke]['ui_color_state']
                            # gray / green / yellow / red
                            #
                        else:
                            #
                            smoke_online = 'offline'
                            battery_health = ''
                            co_alarm_state = ''
                            smoke_alarm_state = ''
                            ui_color_state = ''
                            #
                        #
                        devices_html += urlopen('web/html_devices/{html_smoke}'.format(html_smoke=html_smoke))\
                            .read().encode('utf-8').format(colwidth=colwidth,
                                                           group=str(self._grp_num),
                                                           device=str(self._dvc_num),
                                                           nest_device_id=nest_device_id,
                                                           name=smoke_name,
                                                           online=smoke_online,
                                                           ui_color_state=ui_color_state,
                                                           battery_health=battery_health,
                                                           co_alarm_state=co_alarm_state,
                                                           smoke_alarm_state=smoke_alarm_state)
                        #
                        count += 1
                        #
            #
            # Cameras
            #
            html_cam = get_device_detail(self._type, 'html_cam')
            #
            if html_cam:
                #
                try:
                    cam_ids = json_devices['cameras'].keys()
                except:
                    cam_ids = False
                #
                if bool(cam_ids):
                    count = 0
                    for cam in cam_ids:
                        if count> 0 and count % 4 == 0:
                            devices_html += '</div><div class="row">'
                        #
                        colwidth = '3'
                        rem = len(cam_ids) - count
                        if rem == 1:
                            colwidth = '12'
                        elif rem == 2:
                            colwidth = '6'
                        elif rem == 3:
                            colwidth = '4'
                        #
                        nest_device_id = json_devices['cameras'][cam]['device_id']
                        cam_name = json_devices['cameras'][cam]['name']
                        #
                        if json_devices['cameras'][cam]['is_online']:
                            #
                            cam_online = 'Online'
                            img_color = 'blue'
                            #
                            cam_streaming = json_devices['cameras'][cam]['is_streaming']
                            #
                        else:
                            #
                            cam_online = 'Offline'
                            img_color = 'gray'
                            cam_streaming = ''
                            #
                        #
                        devices_html += urlopen('web/html_devices/{html_cam}'.format(html_cam=html_cam))\
                            .read().encode('utf-8').format(colwidth=colwidth,
                                                           group=str(self._grp_num),
                                                           device=str(self._dvc_num),
                                                           nest_device_id=nest_device_id,
                                                           name=cam_name,
                                                           color=img_color,
                                                           online=cam_online)
                        #
                        count += 1
                        #
            #
            #
        except Exception as e:
            print_error('Nest devices could not be compiled into html - ' + str(e))
        #
        devices_html += '</div>'
        return devices_html

    def getHtml_settings(self, grp_num, dvc_num):
        html = get_device_html_settings(self._type)
        randomstring = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
        #
        try:
            tokexp = self._tokenexpiry().strftime(self._dateformat)
        except:
            tokexp = ''
        #
        if html:
            return urlopen('web/html_settings/devices/' + html).read().encode('utf-8').format(img = self._logo(),
                                                                                              name = self._dvc_name(),
                                                                                              pincode = self._pincode(),
                                                                                              clientid = get_device_detail(self._type, 'client_id'),
                                                                                              state = randomstring,
                                                                                              token = self._token(),
                                                                                              tokenexpiry = tokexp,
                                                                                              dvc_ref='{grpnum}_{dvcnum}'.format(grpnum=grp_num, dvcnum=dvc_num))
        else:
            raise Exception

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
        if bool(self._pincode()):
            if self._checkToken():
                return True
            else:
                return self._getNewToken()
        else:
            return False

    def _tokenexpiry(self):
        try:
            return datetime.datetime.strptime(get_device_config_detail(self._grp_num, self._dvc_num, "tokenexpiry"), self._dateformat)
        except:
            return False

    def _checkToken(self):
        return datetime.datetime.now() < self._tokenexpiry() if bool(self._tokenexpiry()) else False

    def _getNewToken(self):
        url = (self.nesturl_tokenexchange).format(authcode=self._pincode(),
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
            self._updateConfig(data['access_token'],
                               datetime.datetime.now() + datetime.timedelta(milliseconds=data['expires_in']),
                               self._pincode(),
                               get_device_config_detail(self._grp_num, self._dvc_num, "state"))
            #
            return True
        else:
            return False

    def _updateConfig(self, token, tokenexpiry, pincode, state):
        #
        data = json.load(open(os.path.join('config', 'config_devices.json'), 'r'))
        #
        data[str(self._grp_num)]['devices'][str(self._dvc_num)]['details']['token'] = token
        data[str(self._grp_num)]['devices'][str(self._dvc_num)]['details']['tokenexpiry'] = tokenexpiry
        data[str(self._grp_num)]['devices'][str(self._dvc_num)]['details']['pincode'] = pincode
        data[str(self._grp_num)]['devices'][str(self._dvc_num)]['details']['state'] = state
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
        return 'Bearer {authcode}'.format(authcode=self._token())