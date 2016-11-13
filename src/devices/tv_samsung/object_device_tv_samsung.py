import base64
import socket
import time

from src.cfg import my_ip
from src.console_messages import print_command, print_msg

from src.devices.device import Device


#TODO on screen messages - http://tech.shantanugoel.com/2013/07/14/samsung-tv-message-box-python.html


class object_tv_samsung(Device):

    # Used in authentication of socket datagrams
    appstring = "python.iapp.samsung"
    tvappstring = "python..iapp.samsung"
    # What gets reported when it asks for permission
    appname = "HomeControl"

    ALLOWED_BYTES = [chr(0x64), chr(0x00), chr(0x01), chr(0x00)]
    DENIED_BYTES = [chr(0x64), chr(0x00), chr(0x00), chr(0x00)]
    TIMEOUT_BYTES = [chr(0x65), chr(0x00)]

    def __init__ (self, room_id, device_id, q_dvc, queues):
        #
        Device.__init__(self, "tv_samsung", room_id, device_id, q_dvc, queues)
        #
        self.run()


    # TODO
    def getHtml(self, user=False):
        #
        args = {'room_id': self._room_id,
                'device_id': self._device_id}
        #
        return self._getHtml_generic(args)


    #TODO - the following is still to be worked on. Code is based on http://deneb.homedns.org/things/?p=232
    # http://sc0ty.pl/2012/02/samsung-tv-network-remote-control-protocol/
    # SAMSUNG OS/Platform - ORSAY
    # (new OS is Tizen)

    def sendCmd(self, request):
        #
        try:
            #
            cmd = self.commands[request['command']]
            #
            ipencoded = base64.b64encode(my_ip().encode('ascii'))
            # macencoded = base64.b64encode(my_mac())
            #
            # Open Socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self._ipaddress(), 55000))
            #
            ################################
            # Authentication
            sock.send(chr(0x00))
            sock.send(self.writeText(self.appstring))
            sock.send(chr(0x64) + chr(0x00))
            sock.send(self.writeText(ipencoded))
            sock.send(self.writeBase64Text(self.appname))
            sock.send(self.writeBase64Text(self.appname))
            #
            data = sock.recv(4096)
            #
            print(data.encode("ascii"))
            #
            # TODO - check against ALLOWED_BYTES, DENIED_BYTES and TIMEOUT_BYTES
            #
            # msg = chr(0x64) + chr(0x00) + chr(len(ipencoded)) \
            #       + chr(0x00) + ipencoded + chr(len(macencoded)) \
            #       + chr(0x00) + macencoded + chr(len(base64.b64encode(self.appname))) \
            #       + chr(0x00) + base64.b64encode(self.appname)
            # msg = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring + chr(len(msg)) + chr(0x00) + msg
            # sock.send(msg)
            # #
            # data = sock.recv(4096)
            # data = data.encode("UTF-8")
            #
            ################################
            # Send command
            sock.send(chr(0x00))
            sock.send(self.writeText(self.tvappstring))
            sock.send(chr(0x00))
            sock.send(chr(0x00))
            sock.send(chr(0x00))
            sock.send(self.writeBase64Text(cmd))
            #
            data = sock.recv(4096)
            #
            print(data.encode("ascii"))
            #
            #
            # messagepart2 = chr(0xc8) + chr(0x00)
            # part2 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring + chr(len(messagepart2)) + chr(0x00) + messagepart2
            # sock.send(part2)
            # #
            # messagepart3 = chr(0x00) + chr(0x00) + chr(0x00) + chr(len(base64.b64encode(_skey))) + chr(0x00) + base64.b64encode(_skey)
            # part3 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring + chr(len(messagepart3)) + chr(0x00) + messagepart3
            # sock.send(part3)
            #
            ################################
            #
            sock.close()
            #
            response = True
            print_command (cmd,
                           self.dvc_or_acc_id(),
                           self._type,
                           self._ipaddress(),
                           response)
            return response
            #
            ################################
        except:
            print_command (request['command'],
                           self.dvc_or_acc_id(),
                           self._type,
                           self._ipaddress(),
                           'ERROR: Exception encountered')
            return False

    def writeText(self, text):
        return chr(len(text)) + chr(0x00) + text

    def writeBase64Text(self, text):
        return chr(len(base64.b64encode(text.encode("ascii")))) + chr(0x00) + base64.b64encode(text.encode("ascii"))


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
