from send_cmds import sendSOCKET
from enum_remoteTIVO import LSTremote_tivo

class object_TIVO:
    '''TiVo object'''

    def __init__ (self, STRipaddress, INTport, STRaccesskey=""):
        self._STRipaddress = STRipaddress
        self._INTport = INTport
        self._STRaccesskey = STRaccesskey
        self._chan_array_no = 0


    def getIP(self):
        return self._STRipaddress

    def getPort(self):
        return self._INTport

    def getPairingkey(self):
        return self._STRaccesskey

    def setPairingkey(self, STRaccesskey):
        self._STRaccesskey = STRaccesskey

    def getChan_array_no(self):
        return self._chan_array_no


    def sendCmd(self, STRcommand):
        if STRcommand.startswith("FORCECH"):
            return sendSOCKET(self._STRipaddress, self._INTport, STRcommand)
        else:
            comms = LSTremote_tivo
            for x in range(len(comms)):
                if comms[x][0]==STRcommand:
                    return sendSOCKET(self._STRipaddress, self._INTport, comms[x][1])
            return False