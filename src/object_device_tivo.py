from urllib import urlopen
import threading
import requests as requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
import telnetlib
import datetime
import time
from config_devices import get_device_config_detail
from list_devices import get_device_detail, get_device_name, get_device_logo, get_device_html_command, get_device_html_settings
from list_channels import get_channel_item_image_from_devicekey
from web_tvchannels import html_channels_user_and_all
from console_messages import print_command, print_error, print_msg
from tvlisting_getfromqueue import _check_tvlistingsqueue

import cfg


class object_tivo:

    def __init__(self, grp_num, dvc_num, q_dvc, queues):
        #
        self._active = True
        #
        self._type = "tivo"
        self._grp_num = grp_num
        self._dvc_num = dvc_num
        #
        self._queue = q_dvc
        self._q_response_web = queues[cfg.key_q_response_web_device]
        self._q_response_cmd = queues[cfg.key_q_response_command]
        self._q_tvlistings = queues[cfg.key_q_tvlistings]
        #
        self.recordings_timestamp = False
        self.recordings_folders = False
        self.recordings_files = []
        t = threading.Thread(target=self.get_recordings, args=())
        t.daemon = True
        t.start()
        #
        self.run()


    def get_recordings(self):
        while self._active:
            self.recordings_timestamp = datetime.datetime.now()
            self.recordings_folders = self._retrieve_recordings('No').replace(' xmlns="http://www.tivo.com/developer/calypso-protocol-1.6/"','')
            #self.recordings_files = self._retrieve_recordings('Yes', itemCount='&ItemCount=50').replace(' xmlns="http://www.tivo.com/developer/calypso-protocol-1.6/"','')
            #
            ############
            #
            retrieve_items = 50
            #
            files_repeat = True
            loop_count = 0
            itemCount = '&ItemCount={retrieve_items}'.format(retrieve_items=retrieve_items)
            #
            while files_repeat:
                files_count = 0
                files = self._retrieve_recordings('Yes', itemCount=itemCount).replace(' xmlns="http://www.tivo.com/developer/calypso-protocol-1.6/"','')
                xml_files = ET.fromstring(files)
                # Run through individual items
                for item in xml_files.iter('Item'):
                    self.recordings_files.append(item.find('Details'))
                    files_count += 1
                #
                if files_count<50:
                    files_repeat = False
                else:
                    loop_count += 1
                    itemCount = '&ItemCount={retrieve_items}&AnchorOffset={AnchorOffset}'.format(retrieve_items=retrieve_items,
                                                                                                 AnchorOffset=(retrieve_items*loop_count))
            #
            ############
            #
            print_msg('TV recording information retrieved - Group {grp_num} Device {dvc_num}: {type}'.format(grp_num=self._grp_num,
                                                                                                             dvc_num=self._dvc_num,
                                                                                                             type=self._type))
            time.sleep(600) # 600 = 10 minutes


    def run(self):
            time.sleep(5)
            while self._active:
                # Keep in a loop
                '''
                    Use of self._active allows for object to close itself, however may wish
                    to take different approach of terminating the thread the object loop resides in
                '''
                time.sleep(0.1)
                qItem = self._getFromQueue()
                if bool(qItem):
                    if qItem['response_queue'] == 'stop':
                        self._active = False
                    elif qItem['response_queue'] == cfg.key_q_response_web_device:
                        self._q_response_web.put(self.getHtml(user=qItem['user'],
                                                              listings=_check_tvlistingsqueue(self._q_tvlistings)))
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

    def _ipaddress(self):
        return get_device_config_detail(self._grp_num, self._dvc_num, "ipaddress")

    def _port(self):
        return get_device_detail(self._type, "port")

    def _accesskey(self):
        return get_device_config_detail(self._grp_num, self._dvc_num, "mak")

    def _package(self):
        return get_device_config_detail(self._grp_num, self._dvc_num, "package")

    def _logo(self):
        return get_device_logo(self._type)

    def _dvc_name(self):
        return get_device_config_detail(self._grp_num, self._dvc_num, "name")

    def _type_name(self):
        return get_device_name(self._type)

    def _getChan(self):
        response = self._send_telnet(self._ipaddress(), self._port(), response=True)
        if not bool(response):
            return False
        nums = [int(s) for s in response.split() if s.isdigit()]
        return nums[0] if len(nums) > 0 else False

    def sendCmd(self, request):
        #
        try:
            code = False
            response = False
            #
            # if request['command'] == 'getHtml_recordings':
            #     response = self._getHtml_recordings()
            # el
            if request['command'] == 'getchannel':
                response = self._getChan()
            elif request['command'] == 'channel':
                response = self._send_telnet(ipaddress=self._ipaddress(),
                                             port=self._port(),
                                             data=("SETCH {}\r").format(request['chan']),
                                             response=True)
                if response.startswith('CH_FAILED'):
                    print_command('channel', self._type_name(), self._ipaddress(), response)
                    return False
            elif request['command'] == 'command':
                code = self.commands[request['code']]
                try:
                    response = self._send_telnet(self._ipaddress(), self._port(), data=code)
                except:
                    response = False
            #
            x = request['code'] if code else request['command']
            print_command (x, self._type_name(), self._ipaddress(), response)
            return response
        except:
            print_command('channel', self._type_name(), self._ipaddress(), 'ERROR')
            return False

    def getHtml(self, user=False, listings=None):
        #
        html_file = get_device_html_command(self._type)
        #
        chan_current = self._getChan()
        #
        html_channels = html_channels_user_and_all(group_name=self._grp_num,
                                                   device_name=self._dvc_num,
                                                   user=user,
                                                   chan_current=chan_current,
                                                   package=["virginmedia_package", self._package()])
        #
        if self.recordings_timestamp:
            recordings_datetime = self.recordings_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        else:
            recordings_datetime = ''
        #
        return urlopen('web/html_devices/' + html_file).read().encode('utf-8').format(group=self._grp_num,
                                                                                      device=self._dvc_num,
                                                                                      html_recordings=self._getHtml_recordings(),
                                                                                      timestamp_recordings=recordings_datetime,
                                                                                      html_channels=html_channels)

    def getHtml_settings(self, grp_num, dvc_num):
        html_file = get_device_html_settings(self._type)
        if html_file:
            return urlopen('web/html_settings/devices/' + html_file).read().encode('utf-8').format(img=self._logo(),
                                                                                                   name=self._dvc_name(),
                                                                                                   ipaddress=self._ipaddress(),
                                                                                                   mak=self._accesskey(),
                                                                                                   dvc_ref='{grpnum}_{dvcnum}'.format(grpnum=grp_num, dvcnum=dvc_num))
        else:
            return ''

    def _getHtml_recordings(self):
        #
        try:
            # self.recordings_timestamp = datetime.datetime.now()
            # self.recordings_folders = self._retrieve_recordings('No').replace(' xmlns="http://www.tivo.com/developer/calypso-protocol-1.6/"','')
            # self.recordings_files = self._retrieve_recordings('Yes').replace(' xmlns="http://www.tivo.com/developer/calypso-protocol-1.6/"','')
            #
            series = []
            # Run through items in 'folders' xml and identify group/series names, adding to the series[] variable
            if self.recordings_folders:
                xml_folders = ET.fromstring(self.recordings_folders)
                for item in xml_folders.iter('Item'):
                    details = item.find('Details')
                    # details.find('ContentType').text == 'x-tivo-container/folder'
                    if details.find('Title').text != 'Suggestions' and details.find('Title').text != 'HD Recordings':
                        series.append(details.find('Title').text)
            #
            seriesdrop_html = {}
            series_count = {}
            series_type = {}
            movie_rating = {}
            #
            # Build html group containers for adding file html to later.
            if len(series) > 0:
                for title in series:
                    series_count[title] = 0
                    seriesdrop_html[title] = ''
                    series_type[title] = ''
            #
            # Run through items in 'files' xml and commence building html
            if len(self.recordings_files)>0:
                #
                # Run through individual items
                for item in self.recordings_files:
                    #
                    # If part of a series (check against list created above) then create 'folder' group
                    if item.find('Title').text in series:
                        series_count[item.find('Title').text] += 1
                        # not always an episode title!!
                        try:
                            ep_title = item.find('EpisodeTitle').text
                        except Exception as e:
                            ep_title = '-'
                        #
                        try:
                            imgchan = get_channel_item_image_from_devicekey(self._type, int(item.find('SourceChannel').text))
                            img = '<img style="height: 25px;" src="/img/channel/{imgchan}"/>'.format(imgchan=imgchan)
                        except Exception as e:
                            img = False
                        #
                        try:
                            desc = '<div class="row"><div class="col-xs-12"><p>{desc}</p></div></div>'.format(desc=item.find('Description').text)
                        except Exception as e:
                            desc = ''
                        #
                        try:
                            date = int(item.find('CaptureDate').text, 0)
                            date = datetime.datetime.fromtimestamp(date)
                            date = date.strftime('%d-%m-%Y')
                            date = '<div class="row"><div class="col-xs-12"><p>{date}</p></div></div>'.format(date=date)
                        except Exception as e:
                            date = '-'
                        #
                        if item.find('ProgramId').text.startswith('EP'):
                            series_type[item.find('Title').text] = 'series'
                        elif item.find('ProgramId').text.startswith('MV'):
                            series_type[item.find('Title').text] = 'movie'
                            movie_rating[item.find('Title').text] = item.find('MpaaRating').text
                        else:
                            series_type[item.find('Title').text] = '-'
                        #
                        seriesdrop_html[item.find('Title').text] += '<div class="row">'
                        seriesdrop_html[item.find('Title').text] += '<div class="col-xs-9">'
                        seriesdrop_html[item.find('Title').text] += '<h5>{ep_title}</h5>'.format(ep_title=ep_title)
                        seriesdrop_html[item.find('Title').text] += '</div>'
                        seriesdrop_html[item.find('Title').text] += '<div class="col-xs-3" style="text-align: right;">'
                        seriesdrop_html[item.find('Title').text] += '{img}'.format(img=img)
                        seriesdrop_html[item.find('Title').text] += '</div>'
                        seriesdrop_html[item.find('Title').text] += '</div>'
                        seriesdrop_html[item.find('Title').text] += '{desc}'.format(desc=desc)
                        seriesdrop_html[item.find('Title').text] += '{date}'.format(date=date)
                #
                # Run through each item in series_html and add to master html_recordings
                html_recordings = '<div class="row">'
                html_recordings += '<div class="col-xs-10"><h5>Title</h5></div>'
                html_recordings += '<div class="col-xs-2" style="text-align: right;"><h5>#</h5></div>'
                html_recordings += '</div>'
                count = 0
                for title in series:
                    html_recordings += '<div class="row btn-col-grey btn_pointer" style="margin-bottom: 5px;" data-toggle="collapse" data-target="#collapse_series{count}">'.format(count=count)
                    html_recordings += '<div class="col-xs-10"><h5>{title}</h5></div>'.format(title=title)
                    if series_type[title]=='series':
                        html_recordings += '<div class="col-xs-2" style="text-align: right;"><h6>{count}</h6></div>'.format(count=series_count[title])
                    # TODO Movie age rating image removed as uses key as opposed to actual age rating in xml
                    # elif series_type[title]=='movie':
                    #     html_recordings += '<div class="col-xs-2" style="text-align: right; padding: 5px;"><img style="height: 25px;" src="/img/movie_rating/BBFC_{rating}.png"/></div>'.format(rating=movie_rating[title])
                    else:
                        html_recordings += '<div class="col-xs-2" style="text-align: right;"></div>'
                    html_recordings += '</div>'
                    html_recordings += '<div class="row collapse out" id="collapse_series{count}"><div class="container-fluid">{drop}</div></div>'.format(count=count, drop=seriesdrop_html[title])
                    count += 1
                #
                return html_recordings
            else:
                return '<p>Error</p>'
        except Exception as e:
            print_error('Attempted to create recordings html - {error}'.format(error=e))
            return '<p>Error</p>'

    def _retrieve_recordings(self, recurse, itemCount=''):
        try:
            r = requests.get('https://{ipaddress}/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse={recurse}{itemCount}'.format(ipaddress=self._ipaddress(), recurse=recurse, itemCount=itemCount),
                             auth=HTTPDigestAuth('tivo', self._accesskey()),
                             verify=False)
            print_command('retrieve listings (recurse={recurse})'.format(recurse=recurse),
                          self._type,
                          self._ipaddress(),
                          r.status_code)
            if r.status_code == requests.codes.ok:
                return r.content
            else:
                return False
        except Exception as e:
            return False

    def _send_telnet(self, ipaddress, port, data='', response=False):
        try:
            tn = telnetlib.Telnet(ipaddress, port)
            time.sleep(0.1)
            output = tn.read_eager() if response else None
            if data:
                tn.write(str(data)+"\n")
                time.sleep(0.1)
                op = tn.read_eager()
                if op=='':
                    output = True
                else:
                    output = op if (response and not bool(op)) else True
            tn.close()
            return output
        except:
            return False

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
