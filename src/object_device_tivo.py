from send_cmds import sendTELNET
from datetime import datetime
from urllib import urlopen


class object_tivo:
    '''TiVo object'''

    def __init__(self, STRname, STRipaddress, INTport, STRaccesskey=""):
        self._STRipaddress = STRipaddress
        self._INTport = INTport
        self._STRaccesskey = STRaccesskey
        self._type = "tivo"
        self._name = STRname
        self._img = "logo_virgin.png"
        self._tvguide = True

    def getIP(self):
        return self._STRipaddress

    def getPort(self):
        return self._INTport

    def getAccesskey(self):
        return self._STRaccesskey

    def setAccesskey(self, STRaccesskey):
        self._STRaccesskey = STRaccesskey

    def getTvguide_use(self):
        return self._tvguide

    def getType(self):
        return self._type

    def getName(self):
        return self._name

    def getLogo(self):
        return self._img

    def _getChan(self):
        x = sendTELNET(self._STRipaddress, self._INTport, response=True)
        print ("{timestamp} Channel request for TiVo device {ipaddress} - {response}").format(
            timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            ipaddress=self._STRipaddress,
            response=x)
        if not bool(x):
            return False
        nums = [int(s) for s in x.split() if s.isdigit()]
        return nums[0] if len(nums) > 0 else False

    def sendCmd(self, STRcommand):
        if STRcommand == "getchannel":
            return self._getChan()
        elif STRcommand.startswith('go'):
            return sendTELNET(self._STRipaddress,
                              self._INTport,
                              data=("FORCECH {}\r").format(STRcommand.replace('go','')),
                              response=True)
        else:
            try:
                return sendTELNET(self._STRipaddress, self._INTport, data=self.commands[STRcommand])
            except:
                return False

    def getHtml(self, group_name):
        device_url = 'device/{group}/{device}'.format(group=group_name, device=self._name.lower().replace(' ',''))
        return urlopen('web/{page}'.format(page="object_tivo.html")).read().encode('utf-8').format(url=device_url)

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
