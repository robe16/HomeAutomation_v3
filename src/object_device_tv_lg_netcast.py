from urllib import urlopen
import xml.etree.ElementTree as ET
import requests as requests
import time
from list_devices import get_device_name, get_device_detail, get_device_logo, get_device_html_command, get_device_html_settings
from config_devices import get_device_config_detail, set_device_config_detail
from console_messages import print_command, print_msg
import cfg


class object_tv_lg_netcast:

    STRtv_PATHpair = "/udap/api/pairing"
    STRtv_PATHcommand = "/udap/api/command"
    STRtv_PATHevent = "/udap/api/event"
    STRtv_PATHquery = "/udap/api/data"

    def __init__ (self, grp_num, dvc_num, q_dvc, queues):
        self._type = "tv_lg_netcast"
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
                    self._queue.task_done()
            print_msg('Thread stopped - Group {grp_num} Device {dvc_num}: {type}'.format(grp_num=self._grp_num,
                                                                                         dvc_num=self._dvc_num,
                                                                                         type=self._type))

    def _getFromQueue(self):
        if not self._queue.empty():
            return self._queue.get(block=True)
        else:
            return False

    def _ipaddress(self):
        return get_device_config_detail(self._grp_num, self._dvc_num, "ipaddress")

    def _port(self):
        return get_device_detail(self._type, "port")

    def _pairingkey(self):
        return get_device_config_detail(self._grp_num, self._dvc_num, "pairingkey")

    def _logo(self):
        return get_device_logo(self._type)

    def _dvc_name(self):
        return get_device_config_detail(self._grp_num, self._dvc_num, "name")

    def _type_name(self):
        return get_device_name(self._type)

    def _get_paired(self):
        return get_device_config_detail(self._grp_num, self._dvc_num, 'paired')

    def _set_paired(self, status):
        set_device_config_detail(self._grp_num, self._dvc_num, 'paired', status)

    def _pairDevice(self):
        #
        STRxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?><envelope><api type=\"pairing\"><name>hello</name><value>{}</value><port>{}</port></api></envelope>".format(self._pairingkey(), str(self._port()))
        headers = {'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8',
                   'content-type': 'text/xml; charset=utf-8'}
        url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress(), port=str(self._port()), uri=str(self.STRtv_PATHpair))
        #
        r = requests.post(url,
                          STRxml,
                          headers=headers)
        print_command('pairDevice', self._type_name(), url, r.status_code)
        #
        r_pass = True if r.status_code == requests.codes.ok else False
        self._set_paired(r_pass)
        #
        return r_pass

    def _check_paired(self):
        if not self._get_paired():
            count = 0
            while count < 2:
                self._pairDevice()
                if self._get_paired():
                    return True
                count+=1
            if count==5 and not self._get_paired():
                return False
        return True

    def showPairingkey(self):
        #
        STRxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?><envelope><api type=\"pairing\"><name>showKey</name></api></envelope>"
        headers = {'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8',
                   'content-type': 'text/xml; charset=utf-8'}
        url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress(), port=str(self._port()), uri=str(self.STRtv_PATHpair))
        #
        r = requests.post(url,
                          STRxml,
                          headers=headers)
        print_command('showPairingkey', self._type_name(), url, r.status_code)
        #
        r_pass = True if r.status_code == requests.codes.ok else False
        #
        return r_pass

    def getHtml(self):
        html = get_device_html_command(self._type)
        return urlopen('web/html_devices/' + html).read().encode('utf-8').format(group = str(self._grp_num),
                                                                                 device = str(self._dvc_num),
                                                                                 apps = self._html_apps())

    def getHtml_settings(self, grp_num, dvc_num):
        html = get_device_html_settings(self._type)
        if html:
            return urlopen('web/html_settings/devices/' + html).read().encode('utf-8').format(img = self._logo(),
                                                                                              name = self._dvc_name(),
                                                                                              ipaddress = self._ipaddress(),
                                                                                              pairingkey = self._pairingkey,
                                                                                              dvc_ref='{grpnum}_{dvcnum}'.format(grpnum=grp_num, dvcnum=dvc_num))
        else:
            return ''

    def _html_apps(self):
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

                    html += ('<td class="grid_item" style="width: 20%; cursor: pointer; vertical-align: top;" align="center" onclick="sendHttp(\'/command/{group}/{device}?command=app&auid={auid}&name={app_name}\', null, \'GET\', false, true)">' +
                             '<img src="/command/device/{group}/{device}?command=image&auid={auid}&name={app_name}" style="height:50px;"/>' +
                             '<p style="text-align:center; font-size: 13px;">{name}</p>' +
                             '</td>').format(group = str(self._grp_num),
                                             device = str(self._dvc_num),
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
        try:
            #
            if not self._check_paired():
                print_command ('getApplist', self._type_name(), self._ipaddress(), "ERROR: Device could not be paired")
                return False
            #
            uri = "/udap/api/data?target=applist_get&type={type}&index={index}&number={number}".format(type=str(APPtype),
                                                                                                       index=str(APPindex),
                                                                                                       number=str(APPnumber))
            headers = {'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8'}
            url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress(), port=str(self._port()), uri=uri)
            #
            r = requests.get(url, headers=headers)
            print_command('getApplist', self._type_name(), url, r.status_code)
            #
            if not r.status_code == requests.codes.ok:
                self._set_paired(False)
                if not self._check_paired():
                    return False
                r = requests.post(url, headers=headers)
                print_command('getApplist', self._type_name(), url, r.status_code)
            #
            if r.status_code == requests.codes.ok:
                return r.content
            else:
                return False
        except:
            return False
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

    def getAppicon (self, auid, name):
        #
        if not self._check_paired():
            print_command ('getAppicon', self._type_name(), self._ipaddress(), "ERROR: Device could not be paired")
            return False
        #
        # auid = This is the unique ID of the app, expressed as an 8-byte-long hexadecimal string.
        # name = App name
        uri = "/udap/api/data?target=appicon_get&auid={auid}&appname={appname}".format(auid = auid,
                                                                                       appname = name)
        headers = {'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8'}
        url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress(), port=str(self._port()), uri=uri)
        #
        r = requests.get(url, headers=headers)
        print_command('getAppicon', self._type_name(), url, r.status_code)
        #
        if not r.status_code == requests.codes.ok:
            set_device_config_detail(self._grp_num, self._dvc_num, 'paired', False)
            if not self._check_paired():
                return False
            r = requests.post(url, headers=headers)
            print_command('getAppicon', self._type_name(), url, r.status_code)
        #
        if r.status_code == requests.codes.ok:
            return r.content
        else:
            return False

    def getChan(self):
        # sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHquery)+"?target=cur_channel", "close")
        return False

    def sendCmd(self, request):
        #
        try:
            #
            if not self._check_paired():
                print_command (request['command'], self._type_name(), self._ipaddress(), "ERROR: Device could not be paired")
                return False
            #
            if request['command'] == 'image':
                response = self.getAppicon(request['auid'], request['name'].replace(' ','%20'))
                return response
                #
            else:
                if request['command'] == 'app':
                    STRxml = ('<?xml version="1.0" encoding="utf-8"?>' +
                              '<envelope>' +
                              '<api type="command">' +
                              '<name>AppExecute</name>' +
                              '<auid>{auid}</auid>' +
                              '<appname>{app_name}</appname>' +
                              #'<contentId>Content ID</contentId>' +
                              '</api>' +
                              '</envelope>').format(auid = request['auid'],
                                                    app_name = request['name'].replace(' ','%20'))
                    headers = {'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8',
                               'content-type': 'text/xml; charset=utf-8'}
                    cmd = request['command']
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
                print_command('command', self._type_name(), url, r.status_code)
                #
                if not r.status_code == requests.codes.ok:
                    self._set_paired(False)
                    if not self._check_paired():
                        return False
                    r = requests.post(url,
                                      STRxml,
                                      headers=headers)
                    print_command('command', self._type_name(), url, r.status_code)
                #
                response = (r.status_code == requests.codes.ok)
                print_command (cmd, self._type_name(), self._ipaddress(), response)
                return response
                #
        except:
            print_command (request['command'], self._type_name(), self._ipaddress(), "ERROR: Exception encountered")
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