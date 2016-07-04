from send_cmds import sendTELNET, sendHTTP
from urllib import urlopen
from config_devices import get_device_config_detail
from list_devices import get_device_detail, get_device_name, get_device_logo, get_device_html_command, get_device_html_settings
from web_tvlistings import html_listings_user_and_all
from web_tvchannels import html_channels_user_and_all
from console_messages import print_command

from urllib2 import Request, urlopen, HTTPError
from urllib2 import HTTPBasicAuthHandler, HTTPDigestAuthHandler, build_opener, install_opener
import ssl
import hashlib
import random
from console_messages import print_error, print_http
from list_devices import set_device_detail


class object_tivo:

    def __init__(self, label, group):
        self._type = "tivo"
        self._label = label
        self._group = group

    # def getLabel(self):
    #     return self._label
    #
    # def getGroup(self):
    #     return self._group
    #
    # def getType(self):
    #     return self._type

    def _ipaddress(self):
        return get_device_config_detail(self._group.lower().replace(' ',''), self._label.lower().replace(' ',''), "ipaddress")

    def _port(self):
        return get_device_detail(self._type, "port")

    def _accesskey(self):
        return get_device_config_detail(self._group.lower().replace(' ',''), self._label.lower().replace(' ',''), "mak")

    def _logo(self):
        return get_device_logo(self._type)

    def getName(self):
        return get_device_name(self._type)

    def _package(self):
        return get_device_config_detail(self._group.lower().replace(' ',''), self._label.lower().replace(' ',''), "package")

    def _getChan(self):
        response = sendTELNET(self._ipaddress(), self._port(), response=True)
        if not bool(response):
            return False
        nums = [int(s) for s in response.split() if s.isdigit()]
        return nums[0] if len(nums) > 0 else False

    def sendCmd(self, request):
        #
        command = request.query.command
        code = False
        response = False
        #
        if command == 'getchannel':
            response = self._getChan()
        elif command == 'channel':
            response = sendTELNET(self._ipaddress(),
                                  self._port(),
                                  data=("SETCH {}\r").format(request.query.chan),
                                  response=True)
            if response.startswith('CH_FAILED'):
                print_command('channel', get_device_name(self._type), self._ipaddress(), response)
                return False
        elif command == 'command':
            code = self.commands[request.query.code]
            try:
                response = sendTELNET(self._ipaddress(), self._port(), data=code)
            except:
                response = False
        #
        x = request.query.code if code else command
        print_command (x, get_device_name(self._type), self._ipaddress(), response)
        return response

    def getHtml(self, listings=None, user=False):
        #
        html_file = get_device_html_command(self._type)
        #
        chan_current = self._getChan()
        #
        html_channels = html_channels_user_and_all(group_name=self._group.lower().replace(' ',''),
                                                   device_name=self._label.lower().replace(' ',''),
                                                   user=user,
                                                   chan_current=chan_current,
                                                   package=["virginmedia_package", self._package()])
        # html += html_listings_user_and_all(listings,
        #                                    group_name=self._group.lower().replace(' ',''),
        #                                    device_name=self._label.lower().replace(' ',''),
        #                                    user=user,
        #                                    chan_current=chan_current,
        #                                    package=["virginmedia_package", self._package()])
        #
        html = urlopen('web/html_devices/' + html_file).read().encode('utf-8').format(group=self._group.lower().replace(' ',''),
                                                                                      device=self._label.lower().replace(' ',''),
                                                                                      html_channels = html_channels)
        return html

    def getHtml_settings(self, grp_num, dvc_num):
        html = get_device_html_settings(self._type)
        if html:
            print self._ipaddress()
            return urlopen('web/html_settings/devices/' + html).read().encode('utf-8').format(img=self._logo(),
                                                                                              name=self._label,
                                                                                              ipaddress=self._ipaddress(),
                                                                                              mak=self._accesskey(),
                                                                                              dvc_ref='{grpnum}_{dvcnum}'.format(grpnum=grp_num, dvcnum=dvc_num))
        else:
            return ''

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

    def _retrieve_recordings(self):
        recordings = self.sendHTTP_test(self._ipaddress(),
                                        'close',
                                        '/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse=Yes',
                                        password=['tivo', self._accesskey(), 'TiVo DVR'])
        return recordings


    def sendHTTP_test(self, url1a, connection, url2a, method=False, data=False, contenttype=False, header_auth=False, password=False):
        #
        if password:
            authhandler_d = HTTPDigestAuthHandler()
            authhandler_d.add_password(password[2],
                                       url1a + url2a.split('?', 1)[0],
                                       password[0],
                                       password[1])
            authhandler_b = HTTPBasicAuthHandler()
            authhandler_b.add_password(password[2],
                                       url1a + url2a.split('?', 1)[0],
                                       password[0],
                                       password[1])
            opener = build_opener(authhandler_d, authhandler_b)
            install_opener(opener)
        #
        url = 'https://' + url1a + url2a
        #
        if data:
            req = Request(url, data=data)
        else:
            req = Request(url)
        #
        if bool(method):
            req.get_method = lambda: method
        #
        if bool(contenttype):
            req.add_header("content-type", contenttype)
        #
        if bool(header_auth):
            req.add_header("Authorization", header_auth)
        #
        req.add_header("Connection", connection)
        # req.add_header("User-Agent", "Linux/2.6.18 UDAP/2.0 CentOS/5.8")
        #
        #
        # https://www.afpy.org/doc/python/2.7/whatsnew/2.7.html#pep-476-enabling-certificate-verification-by-default-for-stdlib-http-clients
        # 'ssl._create_unverified_context()' is used as per above link to overcome failing ssl certification verification
        #
        #
        # https://docs.python.org/2/howto/urllib2.html#id6
        # if password:
        #     #
        #     ps = HTTPPasswordMgrWithDefaultRealm()
        #     ps.add_password(None, _check_prefix(url1, https), password[0], password[1])
        #     opener = build_opener(HTTPDigestAuthHandler(ps),
        #                           HTTPBasicAuthHandler(ps),
        #                           HTTPSHandler(ssl._create_unverified_context()))
        #     install_opener(opener)
        #
        try:
            x = urlopen(req, timeout=10, context=ssl._create_unverified_context())
            print_http(x.getcode(), 'HTTP request - ' + url)
            return False if not str(x.getcode()).startswith("2") else x
        except HTTPError as h:
            # if str(h.getcode()).startswith("3"):
            #     print_http(h.getcode(), 'Redirect of http request - ' + url + ' - ' + str(h))
            #     url_redirect = h.headers['Location']
            #     if redirect_type:
            #         if url_redirect[-len(url2a):] == url2a:
            #             url_redirect = url_redirect[:(len(url_redirect) - len(url2))]
            #         set_device_detail(redirect_type, 'redirect_url', url_redirect)
            #     return sendHTTP(url_redirect, connection, url2a=url2a, method=method, data=data, contenttype=contenttype,
            #                     header_auth=header_auth, retry=retry + 1)
            # el
            if str(h.getcode()).startswith("401"):
                #
                if password:
                    hd_auth = h.headers['www-authenticate'].split(', ')
                    cookie = h.headers['set-cookie'].split(';', 1)[0]
                    #
                    nc = '00000001'
                    cnonce = hashlib.md5('testcnonce' + str(random.randint(0, 100))).hexdigest()
                    realm = ''
                    nonce = ''
                    qop = ''
                    opaque = ''
                    for item in hd_auth:
                        if item.split("=")[0] == 'Digest realm':
                            realm = item.split("=")[1].strip('"')
                        elif item.split("=")[0] == 'nonce':
                            nonce = item.split("=")[1].strip('"')
                        elif item.split("=")[0] == 'qop':
                            qop = item.split("=")[1].strip('"')
                        elif item.split("=")[0] == 'opaque':
                            opaque = item.split("=")[1].strip('"')
                    #
                    # Digest Authorisation as per https://en.wikipedia.org/wiki/Digest_access_authentication
                    HA1 = hashlib.md5(password[0] + ':' + realm + ':' + password[1]).hexdigest()
                    HA2 = hashlib.md5('GET:' + url2a.split('?', 1)[0]).hexdigest()
                    response = hashlib.md5(
                        HA1 + ':' + nonce + ':' + nc + ':' + cnonce + ':' + qop + ':' + HA2).hexdigest()
                    #
                    header_auth = 'Digest username = "' + password[0] + '", ' + \
                                  'realm = "' + realm + '", ' + \
                                  'nonce = "' + nonce + '", ' + \
                                  'uri = "' + url2a.split('?', 1)[0] + '", ' + \
                                  'qop = "' + qop + '", ' + \
                                  'nc = ' + nc + ', ' + \
                                  'cnonce = "' + cnonce + '", ' + \
                                  'response = "' + response + '", ' + \
                                  'opaque = "' + opaque + '"'
                    req.add_header('Authorization', header_auth)
                    req.add_header('cookie', cookie)
                    # req.add_header("Host", socket.gethostbyname(socket.gethostname()))
                    #
                    #
                    #
                    try:
                        req.add_header('Content-Type', 'application/xml')
                        x = urlopen(req, timeout=10, context=ssl._create_unverified_context())
                        print_http(x.getcode(), 'HTTP request - ' + url)
                        return False if not str(x.getcode()).startswith("2") else x
                    except Exception as e:
                        print_error('Could not send http request - ' + url + ' - ' + str(e))
                        return False
                print_http(h.getcode(), 'Could not send http request - ' + url + ' - ' + str(h))
                return False
        except Exception as e:
            print_error('Could not send http request - ' + url + ' - ' + str(e))
            return False
