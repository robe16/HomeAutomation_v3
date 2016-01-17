from send_cmds import sendHTTP
from urllib import urlopen


class object_tv_lg_netcast:
    '''LG TV object'''

    STRtv_PATHpair = "/udap/api/pairing"
    STRtv_PATHcommand = "/udap/api/command"
    STRtv_PATHevent = "/udap/api/event"
    STRtv_PATHquery = "/udap/api/data"

    def __init__ (self, STRname, STRipaddress, INTport, STRpairingkey=None):
        self._STRipaddress = STRipaddress
        self._INTport = INTport
        self._STRpairingkey = STRpairingkey
        self._type = "lgtv"
        if self._STRpairingkey!=None:
            self._pairDevice()
        self._name = STRname
        self._img = "logo_lg.png"
        self._tvguide = True

    def getIP(self):
        return self._STRipaddress

    def getPort(self):
        return self._INTport

    def getPairingkey(self):
        return self._STRpairingkey

    def setPairingkey(self, STRpairingkey):
        self._STRpairingkey = STRpairingkey
        self._pairDevice()

    def getTvguide_use(self):
        return self._tvguide

    def getType(self):
        return self._type

    def getName(self):
        return self._name

    def getLogo(self):
        return self._img

    def isPaired(self):
        return self._BOOLpaired

    def getHtml(self, group_name):
        device_url = 'device/{group}/{device}'.format(group=group_name, device=self._name.lower().replace(' ',''))
        return urlopen('web/{page}'.format(page="object_lgtv.html")).read().encode('utf-8').format(url=device_url)

    def _pairDevice(self):
        STRxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?><envelope><api type=\"pairing\"><name>hello</name><value>{}</value><port>{}</port></api></envelope>".format(self._STRpairingkey, str(self._INTport))
        x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHpair), "close", data=STRxml)
        self._BOOLpaired = bool(x)
        return self._BOOLpaired

    def showPairingkey(self):
        STRxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?><envelope><api type=\"pairing\"><name>showKey</name></api></envelope>"
        x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHpair), "close", data=STRxml)
        return str(x.getcode()).startswith("2") if bool(x) else False

    def getChan(self):
        # sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHquery)+"?target=cur_channel", "close")
        return False

    def sendCmd(self, STRcommand):
        try:
            data = self.commands[STRcommand]
            if not self._BOOLpaired:
                if not self._repair_device():
                    return False
            STRxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?><envelope><api type=\"command\"><name>HandleKeyInput</name><value>{}</value></api></envelope>".format(data)
            x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHcommand), "close", data=STRxml)
            if bool(x) and not str(x.getcode()).startswith("2"):
                if not self._repair_device():
                    return False
                x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHcommand), "close", data=STRxml)
            return str(x.getcode()).startswith("2") if bool(x) else False
        except:
            return False


    def _repair_device(self):
        count = 0
        while count < 5:
            self._pairDevice()
            if self._BOOLpaired:
                break
            count+=1
        if count==5 and not self._BOOLpaired:
            return False
        return True


    def getApplist(self, APPtype=3, APPindex=0, APPnumber=0):
        # Note - If both index and number are 0, the list of all apps in the category specified by type is fetched.
        # 'APPtype' specifies the category for obtaining the list of apps. The following three values are available.
        #           1: List of all apps
        #           2: List of apps in the Premium category
        #           3: List of apps in the My Apps category
        # 'APPindex' specifies the starting index of the apps list. The value range is from 1 to 1024.
        # 'APPnumber' specifies the number of apps to be obtained from the starting index.
        #             This value has to be greater than or equal to the index value. The value can be from 1 to 1024.
        STRurl = "/udap/api/data?target=applist_get&type={}&index={}&number={}".format(str(APPtype), str(APPindex), str(APPnumber))
        x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+STRurl, "keep-alive")
        if bool(x):
            return x.read() if str(x.getcode()).startswith("2") else False
        else:
            return False

    def getAppicon (self, auid, name):
        # auid = This is the unique ID of the app, expressed as an 8-byte-long hexadecimal string.
        # name = App name
        STRurl = "/udap/api/data?target=appicon_get&auid={}&appname={}".format(auid, name)
        x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+STRurl, "keep-alive")
        if bool(x):
            return x.read() if str(x.getcode()).startswith("2") else False
        else:
            return False

    commands = {"power": "1",
                "0": "2",
                "1": "3",
                "2": "4",
                "3": "5",
                "4": "6",
                "5": "7",
                "6": "8",
                "7": "9",
                "8": "10",
                "9": "11",
                "up": "12",
                "down": "13",
                "left": "14",
                "right": "15",
                "ok": "20",
                "home": "21",
                "menu": "22",
                "prev": "23",
                "volup": "24",
                "voldown": "25",
                "mute": "26",
                "chanup": "27",
                "chandown": "28",
                "blue": "29",
                "green": "30",
                "red": "31",
                "yellow": "32",
                "play": "33",
                "pause": "34",
                "stop": "35",
                "fastforward": "36",
                "rewind": "37",
                "skipforward": "38",
                "skipbackward": "39",
                "record": "40",
                "recordinglist": "41",
                "repeat": "42",
                "livetv": "43",
                "epg": "44",
                "currentprograminfo": "45",
                "aspectratio": "46",
                "externalinput": "47",
                "pipsecondaryvideo": "48",
                "showchangesubtitle": "49",
                "programlist": "50",
                "teletext": "51",
                "mark": "52",
                "3dvideo": "400",
                "3dlr": "401",
                "dash": "402",
                "previouschannelflashback": "403",
                "favouritechannel": "404",
                "quickmenu": "405",
                "textoption": "406",
                "audiodescription": "407",
                "netcastkey": "408",
                "energysaving": "409",
                "avmode": "410",
                "simplink": "411",
                "exit": "412",
                "reservationprogramslist": "413",
                "pipchannelup": "414",
                "pipchanneldown": "415",
                "switchprimarysecondaryvideo": "416",
                "myapps": "417"}