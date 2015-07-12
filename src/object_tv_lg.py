import httplib

from cmd_http import sendHTTP


class object_LGTV:
    '''LG TV object'''

    STRtv_PATHpair = "/udap/api/pairing"
    STRtv_PATHcommand = "/udap/api/command"
    STRtv_PATHevent = "/udap/api/event"

    def __init__ (self, STRipaddress, INTport, STRpairingkey=None):
        self._STRipaddress = STRipaddress
        self._INTport = INTport
        self._STRpairingkey = STRpairingkey
        if self._STRpairingkey!=None:
            self._pairDevice()


    def getIP(self):
        return self._STRipaddress

    def getPort(self):
        return self._INTport

    def getPairingkey(self):
        return self._STRpairingkey
    def setPairingkey(self, STRpairingkey):
        self._STRpairingkey = STRpairingkey
        self._pairDevice()

    def isPaired(self):
        return self._BOOLpaired


    def _pairDevice(self):
        STRxml = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>"
                    +"<envelope>"
                    +"<api type=\"pairing\">"
                    +"<name>hello</name>"
                    +"<value>"+ str(self._STRpairingkey) + "</value>"
                    +"<port>"+ str(self._INTport) +"</port>"
                    +"</api>"
                    +"</envelope>")
        x = sendHTTP(self._STRipaddress+":"+self._INTport+self.STRtv_PATHpair, "close", data=STRxml)
        if not x==False:
            self._BOOLpaired = True
        else:
            self._BOOLpaired = False
        return self._BOOLpaired            


    def showPairingkey(self):
        STRxml = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>"
                    +"<envelope>"
                    +"<api type=\"pairing\">"
                    +"<name>showKey</name>"
                    +"</api>"
                    +"</envelope>")
        x = sendHTTP(self._STRipaddress+":"+self._INTport+self.STRtv_PATHpair, "close", data=STRxml)
        if not x==False:
            return str(x.getcode()).startswith("2")
        else:
            #print ("Error when showing pairing key: "+str(x.reason))
            return False


    def sendCmd(self, STRcommand):
        count = 0
        if not self._BOOLpaired:
            while count < 5:
                self._pairDevice()
                if self._BOOLpaired:
                    break
                count=+1
        if count==5 and not self._BOOLpaired:
            return False
        STRxml = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>"
                    +"<envelope>"
                    +"<api type=\"command\">"
                    +"<name>HandleKeyInput</name>"
                    +"<value>"+ STRcommand + "</value>"
                    +"</api>"
                    +"</envelope>")
        x = sendHTTP(self._STRipaddress+":"+self._INTport+self.STRtv_PATHcommand, "close", data=STRxml)
        if not x==False:
            return str(x.getcode()).startswith("2")
        else:
            #print ("Error when sending command: "+str(x.reason))
            return False
        #code to send command
