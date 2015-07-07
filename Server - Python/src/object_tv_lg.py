from cmd_http import sendHTTP
import httplib

class object_LGTV:
    '''LG TV object'''

    STRtv_PATHshowkey = "/udap/api/pairing"
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
                    +"<value>"+ self._STRpairingkey + "</value>"
                    +"<port>"+ self._INTport +"</port>"
                    +"</api>"
                    +"</envelope>")
        x = sendHTTP(self._STRipaddress+":"+self._INTport, "/udap/api/pairing", "close", data=STRxml)
        if type(x)==httplib.HTTPResponse:
            self._BOOLpaired = str(x.getcode()).startswith("2")
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
        x = sendHTTP(self._STRipaddress+":"+self._INTport, "/udap/api/pairing", "close", data=STRxml)
        if type(x)==httplib.HTTPResponse:
            return str(x.getcode()).startswith("2")
        else:
            print ("Error when showing pairing key: "+str(x.reason))
            return False


    def sendCmd(self):
        if self._BOOLpaired == False:
            self._pairDevice()
        #code to send command
