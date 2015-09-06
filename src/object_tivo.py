from send_cmds import sendSOCKET, sendTELNET
from enum_remoteTIVO import LSTremote_tivo

class object_TIVO:
    '''TiVo object'''

    def __init__ (self, STRname, STRipaddress, INTport, STRaccesskey="", BOOLtvguide_use=False):
        self._STRipaddress = STRipaddress
        self._INTport = INTport
        self._STRaccesskey = STRaccesskey
        self._tvguide_use = BOOLtvguide_use
        self._device = "tivo"
        self._chan_array_no = 0
        self._name = STRname
        self._html = "object-tivo.html"
        self._img = "logo_virgin.png"


    def getIP(self):
        return self._STRipaddress

    def getPort(self):
        return self._INTport

    def getAccesskey(self):
        return self._STRaccesskey

    def setAccesskey(self, STRaccesskey):
        self._STRaccesskey = STRaccesskey

    def getChan_array_no(self):
        return self._chan_array_no

    def getTvguide_use(self):
        return self._tvguide_use

    def getDevice(self):
        return self._device

    def getName(self):
        return self._name

    def getHtml(self):
        return self._html

    def getLogo(self):
        return self._img


    def getChan(self):
        x = sendTELNET(self._STRipaddress, self._INTport, response=True)
        print (("Channel request for TiVo device %s - %s") % (self._STRipaddress, x))
        if not bool(x):
            return False
        nums = [int(s) for s in x.split() if s.isdigit()]
        return nums[0] if len(nums)>0 else False


    def sendCmd(self, STRcommand):
        if STRcommand=="getchannel":
            return self.getChan()
        elif STRcommand.isdigit():
            return sendTELNET(self._STRipaddress, self._INTport, data=("FORCECH {}\r").format(STRcommand), response=True)
        else:
            comms = LSTremote_tivo
            x=0
            while x <len(comms):
                if comms[x][0]==STRcommand:
                    return sendTELNET(self._STRipaddress, self._INTport, data=comms[x][1])
                x+=1
            return False