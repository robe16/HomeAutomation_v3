import datetime
import xml.etree.ElementTree as ET
import requests as requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from multiprocessing import Manager, Process

from src.bundles.devices.device import Device
from src.config.bundles.config_bundles import get_cfg_device_detail
from src.log.console_messages import print_command, print_msg, print_error

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class device_tv_lg_netcast(Device):

    STRtv_PATHpair = '/udap/api/pairing'
    STRtv_PATHcommand = '/udap/api/command'
    STRtv_PATHevent = '/udap/api/event'
    STRtv_PATHquery = '/udap/api/data'

    apps_dict = Manager().dict()

    def __init__ (self, room_id, device_id):
        #
        Device.__init__(self, 'tv_lg_netcast', room_id, device_id)
        #
        self.is_paired = False
        # self._pairDevice()
        #
        self.apps_timestamp = False
        # self.apps_json = False
        # self._get_apps()
        Process(target=self._start_instance).start()

    def _start_instance(self):
        self._pairDevice()
        self._get_apps()

    def _pairingkey(self):
        return get_cfg_device_detail(self._room_id, self._device_id, "pairingkey")

    def _pairDevice(self, pair_reason=''):
        #
        command = 'Device pairing'
        if not pair_reason=='':
            command += '\' - \'{pair_reason}'.format(pair_reason=pair_reason)
        #
        STRxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?><envelope><api type=\"pairing\"><name>hello</name><value>{}</value><port>{}</port></api></envelope>".format(self._pairingkey(), str(self._port()))
        headers = {'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8',
                   'content-type': 'text/xml; charset=utf-8'}
        url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress(), port=str(self._port()), uri=str(self.STRtv_PATHpair))
        #
        try:
            r = requests.post(url,
                              STRxml,
                              headers=headers,
                              timeout=2)
            print_command(command,
                          self.dvc_or_acc_id(),
                          self._type,
                          url,
                          r.status_code)
            #
            r_pass = True if r.status_code == requests.codes.ok else False
            self.is_paired = r_pass
            #
            return r_pass
        except requests.exceptions.ConnectionError as e:
            print_command(command,
                          self.dvc_or_acc_id(),
                          self._type,
                          self._ipaddress(),
                          'ERROR: connection error')
            return False
        except Exception as e:
            print_command(command,
                          self.dvc_or_acc_id(),
                          self._type,
                          self._ipaddress(),
                          'ERROR: {error}'.format(error=e))
            return False

    def _check_paired(self, pair_reason=''):
        if not self.is_paired:
            count = 0
            while count < 2:
                self._pairDevice(pair_reason)
                if self.is_paired:
                    return True
                count+=1
            if count==5 and not self.is_paired:
                return False
        return True

    def showPairingkey(self):
        #
        STRxml = '<?xml version="1.0" encoding="utf-8"?><envelope><api type="pairing"><name>showKey</name></api></envelope>'
        headers = {'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8',
                   'content-type': 'text/xml; charset=utf-8'}
        url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress(), port=str(self._port()), uri=str(self.STRtv_PATHpair))
        #
        r = requests.post(url,
                          STRxml,
                          headers=headers,
                          timeout=2)
        print_command('showPairingkey',
                      self.dvc_or_acc_id(),
                      self._type,
                      url,
                      r.status_code)
        #
        r_pass = True if r.status_code == requests.codes.ok else False
        #
        return r_pass

    def _app_check(self, attempt=1):
        #
        if len(self.apps_dict) == 0 or self.apps_timestamp > (datetime.datetime.now() + datetime.timedelta(minutes = 10)):
            self._get_apps()
        #
        if len(self.apps_dict) > 0:
            return
        elif len(self.apps_dict) == 0 and attempt < 3:
            attempt += 1
            self._app_check(attempt)
        else:
            raise Exception

    def _get_apps(self):
        self.apps_timestamp = datetime.datetime.now()
        self.apps_dict = self._getApplist()
        print_msg('TV Apps list retrieved: {type}'.format(type=self._type), dvc_or_acc_id=self.dvc_or_acc_id())

    def _getApplist(self, APPtype=3, APPindex=0, APPnumber=0):
        try:
            #
            if not self._check_paired(pair_reason='getApplist'):
                return False
            #
            uri = '/udap/api/data?target=applist_get&type={type}&index={index}&number={number}'.format(type=str(APPtype),
                                                                                                       index=str(APPindex),
                                                                                                       number=str(APPnumber))
            headers = {'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8'}
            url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress(), port=str(self._port()), uri=uri)
            #
            r = requests.get(url, headers=headers, timeout=2)
            #
            print_command('getApplist',
                          self.dvc_or_acc_id(),
                          self._type,
                          self._ipaddress(),
                          r.status_code)
            #
            if not r.status_code == requests.codes.ok:
                self.is_paired = False
                if not self._check_paired(pair_reason='getApplist'):
                    return False
                r = requests.post(url, headers=headers, timeout=2)
                print_command('getApplist',
                              self.dvc_or_acc_id(),
                              self._type,
                              self._ipaddress(),
                              r.status_code)
            #
            if r.status_code == requests.codes.ok:
                #
                xml = ET.fromstring(r.content)
                json_apps = {}
                #
                for data in xml[0]:
                    try:
                        json_a = {}
                        json_a['auid'] = data.find('auid').text
                        json_a['name'] = data.find('name').text
                        json_a['type'] = data.find('type').text
                        json_a['cpid'] = data.find('cpid').text
                        json_a['adult'] = data.find('adult').text
                        json_a['icon_name'] = data.find('icon_name').text
                        json_apps[data.find('auid').text] = json_a
                    except:
                        pass
                return json_apps
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

    def getAppicon(self, auid, name):
        #
        if not self._check_paired(pair_reason='getAppicon'):
            return False
        #
        # auid = This is the unique ID of the app, expressed as an 8-byte-long hexadecimal string.
        # name = App name
        uri = '/udap/api/data?target=appicon_get&auid={auid}&appname={appname}'.format(auid = auid,
                                                                                       appname = name)
        headers = {'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8'}
        url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress(), port=str(self._port()), uri=uri)
        #
        r = requests.get(url, headers=headers, timeout=2)
        print_command('getAppicon',
                      self.dvc_or_acc_id(),
                      self._type,
                      self._ipaddress(),
                      r.status_code)
        #
        if not r.status_code == requests.codes.ok:
            self.is_paired = False
            if not self._check_paired(pair_reason='getAppicon'):
                return False
            r = requests.post(url, headers=headers, timeout=2)
            print_command('getAppicon',
                          self.dvc_or_acc_id(),
                          self._type,
                          self._ipaddress(),
                          r.status_code)
        #
        if r.status_code == requests.codes.ok:
            return r.content
        else:
            return False

    def getChan(self):
        # sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHquery)+"?target=cur_channel", "close")
        return False

    def getData(self, request):
        try:
            if request['data'] == 'applist':
                self._app_check()
                return self.apps_dict
        except Exception as e:
            print_error('Failed to return requested data {request} - {error}'.format(request=request['data'],
                                                                                     error=e))
            return False

    def sendCmd(self, request):
        #
        try:
            #
            if not self._check_paired(pair_reason=request['command']):
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
                                  headers=headers,
                                  timeout=2)
                print_command('command',
                              self.dvc_or_acc_id(),
                              self._type,
                              url,
                              r.status_code)
                #
                if not r.status_code == requests.codes.ok:
                    self.is_paired = False
                    if not self._check_paired(pair_reason='command'):
                        return False
                    r = requests.post(url,
                                      STRxml,
                                      headers=headers,
                                      timeout=2)
                    print_command('command',
                                  self.dvc_or_acc_id(),
                                  self._type,
                                  url,
                                  r.status_code)
                #
                response = (r.status_code == requests.codes.ok)
                print_command (cmd,
                               self.dvc_or_acc_id(),
                               self._type,
                               url,
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