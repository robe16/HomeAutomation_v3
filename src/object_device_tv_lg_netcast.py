from send_cmds import sendHTTP
from urllib import urlopen
import xml.etree.ElementTree as ET
from list_devices import get_device_name, get_device_logo, get_device_html_command, get_device_html_settings
from console_messages import print_command


class object_tv_lg_netcast:
    '''LG TV object'''

    STRtv_PATHpair = "/udap/api/pairing"
    STRtv_PATHcommand = "/udap/api/command"
    STRtv_PATHevent = "/udap/api/event"
    STRtv_PATHquery = "/udap/api/data"

    def __init__ (self, label, ipaddress, port, pairingkey=None):
        self._type = "tv_lg_netcast"
        self._label = label
        self._ipaddress = ipaddress
        self._port = port
        self._pairingkey = pairingkey
        if self._pairingkey!=None:
            self._pairDevice()
        self._tvguide = True

    def getType(self):
        return self._type

    def getLabel(self):
        return self._label

    def getIP(self):
        return self._ipaddress

    def getPort(self):
        return self._port

    def getPairingkey(self):
        return self._pairingkey

    def setPairingkey(self, STRpairingkey):
        self._pairingkey = STRpairingkey
        self._pairDevice()

    def getTvguide_use(self):
        return self._tvguide

    def getLogo(self):
        return get_device_logo(self._type)

    def isPaired(self):
        return self._BOOLpaired

    def _pairDevice(self):
        STRxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?><envelope><api type=\"pairing\"><name>hello</name><value>{}</value><port>{}</port></api></envelope>".format(self._pairingkey, str(self._port))
        x = sendHTTP(self._ipaddress+":"+str(self._port)+str(self.STRtv_PATHpair), "close", data=STRxml)
        self._BOOLpaired = bool(x)
        return self._BOOLpaired

    def _check_paired(self):
        if not self._BOOLpaired:
            count = 0
            while count < 5:
                self._pairDevice()
                if self._BOOLpaired:
                    return True
                count+=1
            if count==5 and not self._BOOLpaired:
                return False
        return True

    def showPairingkey(self):
        STRxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?><envelope><api type=\"pairing\"><name>showKey</name></api></envelope>"
        x = sendHTTP(self._ipaddress+":"+str(self._port)+str(self.STRtv_PATHpair), "close", data=STRxml)
        return str(x.getcode()).startswith("2") if bool(x) else False

    def getHtml(self, group_name):
        html = get_device_html_command(self._type)
        return urlopen('web/html_devices/' + html).read().encode('utf-8').format(group = group_name,
                                                                                 device = self._label.lower().replace(' ',''),
                                                                                 apps = self._html_apps(group_name))

    def getHtml_settings(self):
        html = get_device_html_settings(self._type)
        return urlopen('web/html_settings/devices/' + html).read().encode('utf-8').format(img = self.getLogo(),
                                                                                          name = self._label,
                                                                                          ipaddress = self._ipaddress,
                                                                                          pairingkey = self._pairingkey) if html else ''

    def _html_apps(self, group_name):
        #
        if not self._check_paired():
            return '<p style="text-align:center">App list could not be retrieved from the device.</p>'+\
                   '<p style="text-align:center">Please check it is turned on and then try again.</p>'
        #
        applist = self._getApplist()
        #
        if applist:
            #
            html = '<table style="width:100%">' +\
                   '<tr style="height:80px; padding-bottom:2px; padding-top:2px">'
            #
            xml = ET.fromstring(applist)
            #
            count = 1
            for data in xml[0]:
                try:
                    auid = data.find('auid').text
                    name = data.find('name').text
                    type = data.find('type').text
                    cpid = data.find('cpid').text
                    adult = data.find('adult').text
                    icon_name = data.find('icon_name').text
                    #

                    html += ('<td style="width: 20%; cursor: pointer; vertical-align: top;" align="center" onclick="sendHttp(\'/command?group={group}&device={device}&command=app&auid={auid}&name={app_name}\', null, \'GET\', false, true)">' +
                             '<img src="/command?group={group}&device={device}&command=image&auid={auid}&name={app_name}" style="height:50px;"/>' +
                             '<p style="text-align:center; font-size: 13px;">{name}</p>' +
                             '</td>').format(group = group_name,
                                             device = self._label.lower().replace(' ',''),
                                             auid = auid,
                                             app_name = name.replace(' ', '%20'),
                                             name = name)
                    #
                    if count % 4 == 0:
                        html += '</tr><tr style="height:35px; padding-bottom:2px; padding-top:2px">'
                    count += 1
                    #
                except:
                    html += ''
                #
            #
            html += '</table></div>'
            return html
        else:
            return ''

    def _getApplist(self, APPtype=3, APPindex=0, APPnumber=0):
        # http://developer.lgappstv.com/TV_HELP/index.jsp?topic=%2Flge.tvsdk.references.book%2Fhtml%2FUDAP%2FUDAP%2FObtaining+the+Apps+list+Controller+Host.htm
        # Note - If both index and number are 0, the list of all apps in the category specified by type is fetched.
        # 'APPtype' specifies the category for obtaining the list of apps. The following three values are available.
        #           1: List of all apps
        #           2: List of apps in the Premium category
        #           3: List of apps in the My Apps category
        # 'APPindex' specifies the starting index of the apps list. The value range is from 1 to 1024.
        # 'APPnumber' specifies the number of apps to be obtained from the starting index.
        #             This value has to be greater than or equal to the index value. The value can be from 1 to 1024.
        #
        # <?xml version="1.0" encoding="utf-8"?>
        # <envelope>
        #     <dataList name="App List">
        #         <data>
        #             <auid>Unique ID of the app</auid>
        #             <name>app name</name>
        #             <type>category of the app</type>
        #             <cpid>content ID</cpid>
        #             <adult>whether the app is adult all or not</adult>
        #             <icon_name> app icon name</icon_name>
        #         </data>
        #             <!-- Information of different apps are listed-->
        #         <data>
        #         </data>
        #     </dataList>
        # </envelope>
        #
        STRurl = "/udap/api/data?target=applist_get&type={}&index={}&number={}".format(str(APPtype), str(APPindex), str(APPnumber))
        x = sendHTTP(self._ipaddress+":"+str(self._port)+STRurl, "keep-alive")
        if bool(x):
            return x.read() if str(x.getcode()).startswith("2") else False
        else:
            return False

    def getAppicon (self, auid, name):
        # auid = This is the unique ID of the app, expressed as an 8-byte-long hexadecimal string.
        # name = App name
        STRurl = "/udap/api/data?target=appicon_get&auid={auid}&appname={appname}".format(auid = auid,
                                                                                          appname = name)
        x = sendHTTP(self._ipaddress+":"+str(self._port)+STRurl, "keep-alive")
        if bool(x):
            return x.read() if str(x.getcode()).startswith("2") else False
        else:
            return False

    def getChan(self):
        # sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHquery)+"?target=cur_channel", "close")
        return False

    def sendCmd(self, request):
        #
        command = request.query.command
        #
        try:
            #
            if not self._check_paired():
                print_command (command, get_device_name(self._type), self._ipaddress, "ERROR: Device could not be paired")
                return False
            #
            if command == 'image':
                response = self.getAppicon(request.query.auid, request.query.name.replace(' ','%20'))
                print_command (command, get_device_name(self._type), self._ipaddress, bool(response))
                return response
                #
            elif command == 'app':
                STRxml = ('<?xml version="1.0" encoding="utf-8"?>' +
                          '<envelope>' +
                          '<api type="command">' +
                          '<name>AppExecute</name>' +
                          '<auid>{auid}</auid>' +
                          '<appname>{app_name}</appname>' +
                          #'<contentId>Content ID</contentId>' +
                          '</api>' +
                          '</envelope>').format(auid = request.query.auid,
                                                app_name = request.query.name.replace(' ','%20'))
                response = sendHTTP(self._ipaddress+":"+str(self._port)+str(self.STRtv_PATHcommand), "close", data=STRxml)
                if bool(response) and not str(response.getcode()).startswith("2"):
                    if not self._check_paired():
                        return False
                    response = sendHTTP(self._ipaddress+":"+str(self._port)+str(self.STRtv_PATHcommand), "close", data=STRxml)
                #
                response = str(response.getcode()).startswith("2") if bool(response) else False
                print_command (command, get_device_name(self._type), self._ipaddress, bool(response))
                return response
                #
            else:
                code = self.commands[request.query.command]
                STRxml = ('<?xml version="1.0" encoding="utf-8"?>' +
                          '<envelope>' +
                          '<api type="command">' +
                          '<name>HandleKeyInput</name>' +
                          '<value>{value}</value>' +
                          '</api>' +
                          '</envelope>').format(value = code)
                response = sendHTTP(self._ipaddress+":"+str(self._port)+str(self.STRtv_PATHcommand), "close", data=STRxml)
                if bool(response) and not str(response.getcode()).startswith("2"):
                    if not self._check_paired():
                        return False
                    response = sendHTTP(self._ipaddress+":"+str(self._port)+str(self.STRtv_PATHcommand), "close", data=STRxml)
                #
                response = str(response.getcode()).startswith("2") if bool(response) else False
                print_command (code, get_device_name(self._type), self._ipaddress, bool(response))
                return response
                #
        except:
            print_command (command, get_device_name(self._type), self._ipaddress, "ERROR: Exception encountered")
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