class object_NEST_SMOKE:
    '''Nest Smoke Detector Object'''

    def __init__ (self, STRstructureid, STRdeviceid, STRdevicename, STRdevicenamelong, BOOLonline, STRbattery_health, STRco_alarm_state, STRsmoke_alarm_state, BOOLis_manual_test_active, last_manual_test_time, ui_color_state):
        self._STRstructureid = STRstructureid
        self._STRdeviceid = STRdeviceid
        self._STRdevicename = STRdevicename
        self._STRdevicenamelong = STRdevicenamelong
        self._BOOLonline = BOOLonline
        self._STRbattery_health = STRbattery_health
        self._STRco_alarm_state = STRco_alarm_state
        self._STRsmoke_alarm_state = STRsmoke_alarm_state
        self._BOOLis_manual_test_active = BOOLis_manual_test_active
        self._last_manual_test_time = last_manual_test_time
        self._ui_color_state = ui_color_state


    def StructureID(self):
        return self._STRstructureid

    def DeviceID(self):
        return self._STRdeviceid

    def DeviceName(self):
        return self._STRdevicename

    def DeviceNameLong(self):
        return self._STRdevicenamelong

    def isOnline(self):
        return self._BOOLonline

    def BatteryHealth(self):
        return self._STRbattery_health

    def CO_alarmState(self):
        return self._STRco_alarm_state

    def Smoke_alarmState(self):
        return self._STRsmoke_alarm_state

    def isManualTestActive(self):
        return self._BOOLis_manual_test_active

    def LastManualTestTime(self):
        return self._last_manual_test_time

    def UIcolorState(self):
        return self._ui_color_state


    def sendCmd(self):
        #code to send command
        return False
