#from cmd_tcp import sendTCP

class object_TIVO:
    '''TiVo object'''

    def __init__ (self, STRipaddress, INTport, STRaccesskey=""):
        self._STRipaddress = STRipaddress
        self._INTport = INTport
        self._STRaccesskey = STRaccesskey


    def getIP(self):
        return self._STRipaddress

    def getPort(self):
        return self._INTport

    def getPairingkey(self):
        return self._STRaccesskey

    def setPairingkey(self, STRaccesskey):
        self._STRaccesskey = STRaccesskey

    
    def sendCmd(self):
        #TODO
        return False
