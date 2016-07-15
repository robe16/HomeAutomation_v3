from urllib import urlopen
from config_devices import get_device_config_detail
from list_devices import get_device_detail, get_device_name, get_device_logo, get_device_html_command, get_device_html_settings
from list_channels import get_channel_item_image_from_devicekey
from web_tvchannels import html_channels_user_and_all
from console_messages import print_command, print_error
import requests as requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
import telnetlib
import time
import datetime


class object_tivo:

    def __init__(self, label, group):
        self._type = "tivo"
        self._label = label
        self._group = group

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
        response = self._send_telnet(self._ipaddress(), self._port(), response=True)
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
        if command == 'getHtml_recordings':
            response = self._getHtml_recordings()
        elif command == 'getchannel':
            response = self._getChan()
        elif command == 'channel':
            response = self._send_telnet(ipaddress=self._ipaddress(),
                                         port=self._port(),
                                         data=("SETCH {}\r").format(request.query.chan),
                                         response=True)
            if response.startswith('CH_FAILED'):
                print_command('channel', get_device_name(self._type), self._ipaddress(), response)
                return False
        elif command == 'command':
            code = self.commands[request.query.code]
            try:
                response = self._send_telnet(self._ipaddress(), self._port(), data=code)
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
        #
        url = "'/command?group={group}&device={device}&command=getHtml_recordings'".format(group=self._group.lower().replace(' ',''),
                                                                                                 device=self._label.lower().replace(' ',''))
        #
        html_recordings = "<script type='text/javascript'>" + \
                          "window.onload = function checkRecordings(url){" + \
                              "var xmlHttp = new XMLHttpRequest();" + \
                              "xmlHttp.open('GET', " + url + ", false);" + \
                              "xmlHttp.send(null);" + \
                              "if (xmlHttp.status==200) {" + \
                              "document.getElementById('tivo_recordings').innerHTML=xmlHttp.responseText}" + \
                              "else {setTimeout(function () {checkRecordings(" + url + ");}, 5000);}" + "}" + \
                          "</script>"
        #
        return urlopen('web/html_devices/' + html_file).read().encode('utf-8').format(group=self._group.lower().replace(' ',''),
                                                                                      device=self._label.lower().replace(' ',''),
                                                                                      html_recordings = html_recordings,
                                                                                      html_channels = html_channels)

    def getHtml_settings(self, grp_num, dvc_num):
        html_file = get_device_html_settings(self._type)
        if html_file:
            return urlopen('web/html_settings/devices/' + html_file).read().encode('utf-8').format(img=self._logo(),
                                                                                                   name=self._label,
                                                                                                   ipaddress=self._ipaddress(),
                                                                                                   mak=self._accesskey(),
                                                                                                   dvc_ref='{grpnum}_{dvcnum}'.format(grpnum=grp_num, dvcnum=dvc_num))
        else:
            return ''

    def _getHtml_recordings(self):
        #
        try:
            recordings_folders = self._retrieve_recordings('No').replace(' xmlns="http://www.tivo.com/developer/calypso-protocol-1.6/"','')
            recordings_files = self._retrieve_recordings('Yes').replace(' xmlns="http://www.tivo.com/developer/calypso-protocol-1.6/"','')
            #
            series = []
            # Run through items in 'folders' xml and identify group/series names, adding to the series[] variable
            if recordings_folders:
                xml_folders = ET.fromstring(recordings_folders)
                for item in xml_folders.iter('Item'):
                    details = item.find('Details')
                    # details.find('ContentType').text == 'x-tivo-container/folder'
                    if details.find('Title').text != 'Suggestions' and details.find('Title').text != 'HD Recordings':
                        series.append(details.find('Title').text)
            #
            seriesdrop_html = {}
            series_count = {}
            # Build html group containers for adding file html to later.
            if len(series) > 0:
                for title in series:
                    series_count[title] = 0
                    seriesdrop_html[title] = ''
            #
            # Run through items in 'files' xml and commence building html
            if recordings_files:
                xml_files = ET.fromstring(recordings_files)
                #
                # Run through individual items
                for item in xml_files.iter('Item'):
                    details = item.find('Details')
                    #
                    # If part of a series (check against list created above) then create 'folder' group
                    if details.find('Title').text in series:
                        series_count[details.find('Title').text] += 1
                        # not always an episode title!!
                        try:
                            ep_title = details.find('EpisodeTitle').text
                        except Exception as e:
                            ep_title = '-'
                        #
                        try:
                            imgchan = get_channel_item_image_from_devicekey(self._type, int(details.find('SourceChannel').text))
                            img = '<img style="height: 25px;" src="/img/channel/{imgchan}"/>'.format(imgchan=imgchan)
                        except Exception as e:
                            img = False
                        #
                        try:
                            desc = '<div class="row"><div class="col-xs-12"><p>{desc}</p></div></div>'.format(desc=details.find('Description').text)
                        except Exception as e:
                            desc = ''
                        #
                        try:
                            date = int(details.find('CaptureDate').text, 0)
                            date = datetime.datetime.fromtimestamp(date)
                            date = date.strftime('%d-%m-%Y')
                            date = '<div class="row"><div class="col-xs-12"><p>{date}</p></div></div>'.format(date=date)
                        except Exception as e:
                            date = '-'
                        #
                        seriesdrop_html[details.find('Title').text] += '<div class="row">'
                        seriesdrop_html[details.find('Title').text] += '<div class="col-xs-9">'
                        seriesdrop_html[details.find('Title').text] += '<h5>{ep_title}</h5>'.format(ep_title=ep_title)
                        seriesdrop_html[details.find('Title').text] += '</div>'
                        seriesdrop_html[details.find('Title').text] += '<div class="col-xs-3" style="text-align: right;">'
                        seriesdrop_html[details.find('Title').text] += '{img}'.format(img=img)
                        seriesdrop_html[details.find('Title').text] += '</div>'
                        seriesdrop_html[details.find('Title').text] += '</div>'
                        seriesdrop_html[details.find('Title').text] += '{desc}'.format(desc=desc)
                        seriesdrop_html[details.find('Title').text] += '{date}'.format(date=date)
                    #
                #
                # Run through each item in series_html and add to master html_recordings
                html_recordings = '<div class="container-fluid"><div class="row">'
                html_recordings += '<div class="col-xs-10"><h5>Title</h5></div>'
                html_recordings += '<div class="col-xs-2" style="text-align: right;"><h5>#</h5></div>'
                html_recordings += '</div>'
                count = 0
                for title in series:
                    html_recordings += '<div class="row btn-col-grey btn_pointer" style="margin-bottom: 5px;" data-toggle="collapse" data-target="#collapse_series{count}">'.format(count=count)
                    html_recordings += '<div class="col-xs-10"><h5>{title}</h5></div>'.format(title=title)
                    html_recordings += '<div class="col-xs-2" style="text-align: right;"><h6>{count}</h6></div>'.format(count=series_count[title])
                    html_recordings += '</div>'
                    html_recordings += '<div class="row collapse out" id="collapse_series{count}"><div class="container-fluid">{drop}</div></div>'.format(count=count, drop=seriesdrop_html[title])
                    count += 1
                html_recordings += '</div>'
                #
                return html_recordings
            else:
                return '<p>Error</p>'
        except Exception as e:
            print_error('Attempted to create recordings html - {error}'.format(error=e))
            return '<p>Error</p>'
    #
    # <?xml version="1.0" encoding="utf-8"?>
    #   <TiVoContainer xmlns="http://www.tivo.com/developer/calypso-protocol-1.6/">
    #       <Details>
    #           <ContentType>x-tivo-container/tivo-videos</ContentType>
    #           <SourceFormat>x-tivo-container/tivo-dvr</SourceFormat>
    #           <Title>Now Playing</Title>
    #           <LastChangeDate>0x577D7A25</LastChangeDate>
    #           <TotalItems>18</TotalItems>
    #           <UniqueId>/NowPlaying</UniqueId>
    #       </Details>
    #       <SortOrder>Type,CaptureDate</SortOrder>
    #       <GlobalSort>Yes</GlobalSort>
    #       <ItemStart>0</ItemStart>
    #       <ItemCount>16</ItemCount>
    #       <Item>
    #           <Details>
    #               <ContentType>video/x-tivo-raw-tts</ContentType>
    #               <SourceFormat>video/x-tivo-raw-tts</SourceFormat>
    #               <Title>24 Hours in A&amp;E</Title>
    #               <CopyProtected>Yes</CopyProtected>
    #               <SourceSize>4729077760</SourceSize>
    #               <Duration>3899000</Duration>
    #               <CaptureDate>0x577D6302</CaptureDate>
    #               <ShowingDuration>3600000</ShowingDuration>
    #               <StartPadding>60000</StartPadding>
    #               <EndPadding>240000</EndPadding>
    #               <ShowingStartTime>0x577D6340</ShowingStartTime>
    #               <Description>Cyclist Athar, who's 22, is rushed to St George's...</Description>
    #               <SourceChannel>142</SourceChannel>
    #               <SourceStation>4 HD</SourceStation>
    #               <HighDefinition>Yes</HighDefinition>
    #               <ProgramId>EP014129450131</ProgramId>
    #               <SeriesId>SH01412945</SeriesId>
    #               <StreamingPermission>Yes</StreamingPermission>
    #               <ShowingBits>20996</ShowingBits>
    #               <SourceType>2</SourceType>
    #               <IdGuideSource>50716</IdGuideSource>
    #           </Details>
    #           <Links>
    #               <Content>
    #                   <Url>http://192.168.0.111:80/download/24%20Hours%20in%20A%26E.TiVo?Container=%2FNowPlaying&amp;id=1360</Url>
    #                   <ContentType>video/x-tivo-raw-tts</ContentType>
    #                   <Available>No</Available>
    #               </Content><CustomIcon>
    #               <Url>urn:tivo:image:save-until-i-delete-recording</Url>
    #               <ContentType>image/*</ContentType>
    #               <AcceptsParams>No</AcceptsParams>
    #               </CustomIcon><TiVoVideoDetails>
    #               <Url>https://192.168.0.111:443/TiVoVideoDetails?id=1360</Url>
    #               <ContentType>text/xml</ContentType>
    #               <AcceptsParams>No</AcceptsParams>
    #               </TiVoVideoDetails>
    #           </Links>
    #       </Item>
    #       <Item>
    #               etc.
    #       </Item>
    #   </TiVoContainer>
    #

    def _retrieve_recordings(self, recurse):
        try:
            r = requests.get('https://{ipaddress}/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse={recurse}'.format(ipaddress=self._ipaddress(), recurse=recurse),
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