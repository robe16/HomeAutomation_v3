from send_cmds import sendTELNET
from datetime import datetime
from urllib import urlopen
from list_devices import get_device_logo, get_device_html_command, get_device_html_settings


class object_tivo:
    '''TiVo object'''

    def __init__(self, label, ipaddress, port, accesskey=""):
        self._type = "tivo"
        self._label = label
        self._ipaddress = ipaddress
        self._port = port
        self._accesskey = accesskey
        self._tvguide = True

    def getLabel(self):
        return self._label

    def getType(self):
        return self._type

    def getIP(self):
        return self._ipaddress

    def getPort(self):
        return self._port

    def getAccesskey(self):
        return self._STRaccesskey

    def setAccesskey(self, STRaccesskey):
        self._STRaccesskey = STRaccesskey

    def getTvguide_use(self):
        return self._tvguide

    def getLogo(self):
        return get_device_logo(self._type)

    def _getChan(self):
        x = sendTELNET(self._ipaddress, self._port, response=True)
        print ("{timestamp} Channel request for TiVo device {ipaddress} - {response}").format(
            timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            ipaddress=self._ipaddress,
            response=x)
        if not bool(x):
            return False
        nums = [int(s) for s in x.split() if s.isdigit()]
        return nums[0] if len(nums) > 0 else False

    def sendCmd(self, request):
        #
        command = request.query.command
        #
        if command == "getchannel":
            return self._getChan()
        elif command == "channel":
            return sendTELNET(self._ipaddress,
                              self._port,
                              data=("FORCECH {}\r").format(request.query.chan),
                              response=True)
        elif command == 'command':
            code = self.commands[request.query.code]
            try:
                return sendTELNET(self._ipaddress, self._port, data=code)
            except:
                return False

    def getHtml(self, group_name):
        html = get_device_html_command(self._type)
        return urlopen('web/html_devices/' + html).read().encode('utf-8').format(group=group_name,
                                                                                 device=self._label.lower().replace(' ',''))

    def getHtml_settings(self):
        html = get_device_html_settings(self._type)
        return urlopen('web/html_settings/devices/' + html).read().encode('utf-8').format(img = self.getLogo(),
                                                                                          name = self._label,
                                                                                          ipaddress = self._ipaddress,
                                                                                          mak = self._accesskey) if html else ''

    commands = {"power": "IRCODE STANDBY\r",
                "1": "IRCODE NUM1\r",
                "2": "IRCODE NUM2\r",
                "3": "IRCODE NUM3\r",
                "4": "IRCODE NUM4\r",
                "5": "IRCODE NUM5\r",
                "6": "IRCODE NUM6\r",
                "7": "IRCODE NUM7\r",
                "8": "IRCODE NUM8\r",
                "9": "IRCODE NUM9\r",
                "0": "IRCODE NUM0\r",
                "home": "IRCODE TIVO\r",
                "livetv": "IRCODE LIVETV\r",
                "myshows": "IRCODE NOWSHOWING\r",
                "info": "IRCODE INFO\r",
                "zoom": "IRCODE ZOOM\r",
                "guide": "IRCODE GUIDE\r",
                "subtitles": "IRCODE CC_ON\r",
                "up": "IRCODE UP\r",
                "down": "IRCODE DOWN\r",
                "left": "IRCODE LEFT\r",
                "right": "IRCODE RIGHT\r",
                "select": "IRCODE SELECT\r",
                "channelup": "IRCODE CHANNELUP\r",
                "channeldown": "IRCODE CHANNELDOWN\r",
                "thumbsup": "IRCODE THUMBSUP\r",
                "thumbsdown": "IRCODE THUMBSDOWN\r",
                "record": "IRCODE RECORD\r",
                "play": "IRCODE PLAY\r",
                "pause": "IRCODE PAUSE\r",
                "stop": "IRCODE STOP\r",
                "reverse": "IRCODE REVERSE\r",
                "forward": "IRCODE FORWARD\r",
                "slow": "IRCODE SLOW\r",
                "back": "IRCODE REPLAY\r",
                "next": "IRCODE ADVANCE\r",
                "actiona": "IRCODE ACTION_A\r",
                "actionb": "IRCODE ACTION_B\r",
                "actionc": "IRCODE ACTION_C\r",
                "actiond": "IRCODE ACTION_D\r",
                "clear": "IRCODE CLEAR\r",
                "enter": "IRCODE ENTER\r"}
