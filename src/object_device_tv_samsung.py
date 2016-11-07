from urllib import urlopen
import requests as requests
import telnetlib
import time
from list_devices import get_device_name, get_device_detail, get_device_logo, get_device_html_command, get_device_html_settings
from config_devices import get_cfg_device_detail, set_cfg_device_detail
from console_messages import print_command, print_msg
import cfg

import socket
from uuid import getnode as get_mac
import base64


class object_tv_samsung:

    STRtv_PATHcommand = ''

    def __init__ (self, structure_id, room_id, device_id, q_dvc, queues):
        #
        self._type = "tv_samsung"
        self._structure_id = structure_id
        self._room_id = room_id
        self._device_id = device_id
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
                    self._queue.task_done()
            print_msg('Thread stopped - Structure "{structure_id}" Room "{room_id}" Device "{device_id}": {type}'.format(structure_id=self._structure_id,
                                                                                                                         room_id=self._room_id,
                                                                                                                         device_id=self._device_id,
                                                                                                                         type=self._type))

    def _getFromQueue(self):
        if not self._queue.empty():
            return self._queue.get(block=True)
        else:
            return False

    def dvc_or_acc_id(self):
        return self._structure_id + ':' + self._room_id + ':' + self._device_id

    def _ipaddress(self):
        return get_cfg_device_detail(self._structure_id, self._room_id, self._device_id, "ipaddress")

    def _port(self):
        return get_device_detail(self._type, "port")

    def _pairingkey(self):
        return get_cfg_device_detail(self._structure_id, self._room_id, self._device_id, "pairingkey")

    def _logo(self):
        return get_device_logo(self._type)

    def _dvc_name(self):
        return get_cfg_device_detail(self._structure_id, self._room_id, self._device_id, "name")

    def _type_name(self):
        return get_device_name(self._type)

    # TODO
    def getHtml(self):
        html = get_device_html_command(self._type)
        return urlopen('web/html_devices/' + html).read().encode('utf-8').format(structure_id=self._structure_id,
                                                                                 room_id=self._room_id,
                                                                                 device_id=self._device_id)

    #TODO
    def sendCmd(self, request):
        #
        try:
            #
            if request['command'] == 'image':
                True
            else:
                code = self.commands[request['command']]
                STRxml = ('<?xml version="1.0" encoding="utf-8"?>' +
                          '<envelope>' +
                          '<api type="command">' +
                          '<name>HandleKeyInput</name>' +
                          '<value>{value}</value>' +
                          '</api>' +
                          '</envelope>').format(value=code)
                headers = {'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8',
                           'content-type': 'text/xml; charset=utf-8'}
                cmd = request['command']
                #
                url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress(),
                                                              port=str(self._port()),
                                                              uri=str(self.STRtv_PATHcommand))
                r = requests.post(url,
                                  STRxml,
                                  headers=headers)
                print_command('command',
                              self.dvc_or_acc_id(),
                              self._type,
                              self._ipaddress(),
                              r.status_code)
                #
                response = (r.status_code == requests.codes.ok)
                print_command (cmd,
                               self.dvc_or_acc_id(),
                               self._type,
                               self._ipaddress(),
                               response)
                return response
                #
        except:
            print_command (request['command'],
                           self.dvc_or_acc_id(),
                           self._type,
                           self._ipaddress(),
                           'ERROR: Exception encountered')
            return False



    #TODO - the following is still to be worked on. Code is based on http://deneb.homedns.org/things/?p=232
    # SAMSUNG OS/Platform - ORSAY
    # (new OS is Tizen)

    # What the iPhone app reports
    appstring = "iphone..iapp.samsung"
    # Might need changing to match your TV type
    tvappstring = "iphone.UE55C8000.iapp.samsung"
    # What gets reported when it asks for permission
    remotename = "Python Samsung Remote"


    def sendCmd_new(self, cmd):
        #
        myip = socket.gethostbyname(socket.gethostname())
        mymac = ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
        #
        _skey = code = self.commands[cmd]
        #
        # First configure the connection
        ipencoded = base64.b64encode(myip)
        macencoded = base64.b64encode(mymac)
        messagepart1 = chr(0x64) + chr(0x00) + chr(len(ipencoded)) \
                       + chr(0x00) + ipencoded + chr(len(macencoded)) + chr(0x00) \
                       + macencoded + chr(len(base64.b64encode(self.remotename))) + chr(0x00) \
                       + base64.b64encode(self.remotename)
        #
        part1 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring + chr(len(messagepart1)) + chr(0x00) + messagepart1
        #
        messagepart2 = chr(0xc8) + chr(0x00)
        part2 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring + chr(len(messagepart2)) + chr(0x00) + messagepart2
        #
        messagepart3 = chr(0x00) + chr(0x00) + chr(0x00) + chr(len(base64.b64encode(_skey))) + chr(0x00) + base64.b64encode(_skey)
        part3 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring + chr(len(messagepart3)) + chr(0x00) + messagepart3
        #
        # Create data array to send via socket/telnet
        data = []
        data[0] = part1
        data[1] = part2
        data[2] = part3
        #
        # Send commands
        self._send_telnet(data)

    def _send_telnet(self, data, response=False):
        try:
            tn = telnetlib.Telnet(self._ipaddress(), 55000)
            time.sleep(0.1)
            output = tn.read_eager() if response else None
            #
            x = 0
            while x < len(data):
                if data[x]:
                    tn.write(str(data[x])+"\n")
                    time.sleep(0.1)
                    op = tn.read_eager()
                    if op=='':
                        output = True
                    else:
                        output = op if (response and not bool(op)) else True
                x += 1
            tn.close()
            return output
        except:
            return False



    commands = {"power": "KEY_POWEROFF",
                "0": "KEY_0",
                "1": "KEY_1",
                "2": "KEY_2",
                "3": "KEY_3",
                "4": "KEY_4",
                "5": "KEY_5",
                "6": "KEY_6",
                "7": "KEY_7",
                "8": "KEY_8",
                "9": "KEY_9",
                "aspect": "KEY_ASPECT",
                "ratio43": "KEY_4_3",
                "ratio169": "KEY_16_9",
                "applist": "KEY_APP_LIST",
                "av1": "KEY_AV1",
                "av2": "KEY_AV2",
                "av3": "KEY_AV3",
                "component1": "KEY_COMPONENT1",
                "component2": "KEY_COMPONENT2",
                "hdmi": "KEY_HDMI",
                "hdmi1": "KEY_HDMI1",
                "hdmi2": "KEY_HDMI2",
                "hdmi3": "KEY_HDMI3",
                "hdmi4": "KEY_HDMI4",
                "up": "KEY_UP",
                "down": "KEY_DOWN",
                "left": "KEY_LEFT",
                "right": "KEY_RIGHT",
                "enter": "KEY_ENTER",
                "home": "KEY_HOME",
                "menu": "KEY_MENU",
                "tools": "KEY_TOOLS",
                "clear": "KEY_CLEAR",
                "return": "KEY_RETURN",
                "volup": "KEY_UP",
                "voldown": "KEY_VOLDOWN",
                "mute": "KEY_MUTE",
                "chanup": "KEY_CHUP",
                "chandown": "KEY_CHDOWN",
                "blue": "KEY_CYAN",
                "green": "KEY_GREEN",
                "red": "KEY_RED",
                "yellow": "KEY_YELLOW",
                "play": "KEY_PLAY",
                "pause": "KEY_PAUSE",
                "stop": "KEY_STOP",
                "rewind": "KEY_REWIND",
                "record": "KEY_REC"}
