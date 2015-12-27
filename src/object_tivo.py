from send_cmds import sendTELNET
from list_remotes_retriever import read_list_remotes
from datetime import datetime

class object_TIVO:
    '''TiVo object'''

    def __init__ (self, STRname, STRipaddress, INTport, STRaccesskey="", BOOLtvguide_use=False):
        self._STRipaddress = STRipaddress
        self._INTport = INTport
        self._STRaccesskey = STRaccesskey
        self._tvguide_use = BOOLtvguide_use
        self._type = "tivo"
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

    def getTvguide_use(self):
        return self._tvguide_use

    def getType(self):
        return self._type

    def getName(self):
        return self._name

    def getHtml(self):
        return self._html

    def getLogo(self):
        return self._img


    def getChan(self):
        x = sendTELNET(self._STRipaddress, self._INTport, response=True)
        print ("{timestamp} Channel request for TiVo device {ipaddress} - {response}").format(timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                                                                              ipaddress=self._STRipaddress,
                                                                                              response=x)
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
            data = read_list_remotes(self._type, STRcommand)
            return sendTELNET(self._STRipaddress, self._INTport, data=data) if data else False