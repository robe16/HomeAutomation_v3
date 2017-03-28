from bindings.info_service import InfoService
from log.console_messages import print_error
from config.bindings.config_bindings import get_cfg_info_detail_private
import json
from data_source_metoffice import createForecast
from data_source_sunrise_sunset_org import createSunriseSet


class info_metoffice(InfoService):

    def __init__ (self, info_seq):
        #
        InfoService.__init__(self, 'weather', info_seq)

    def getData(self, request):
        try:
            if request['data'] == 'forecast':
                return json.dumps(self.getForecast())
        except Exception as e:
            print_error('Failed to return requested data {request} - {error}'.format(request=request['data'],
                                                                                     error=e))
            return False

    def getForecast(self):
        #
        town = get_cfg_info_detail_private(self._info_seq, 'town')
        forecast = createForecast(town)
        #
        lat = forecast['location']['latitude']
        lng = forecast['location']['longitude']
        #
        day = 0
        while day < len(forecast['days']):
            #
            forecast['days'][day]['sunRiseSet'] = createSunriseSet(forecast['days'][day]['date'],
                                                                   lat,
                                                                   lng)
            #
            day += 1
            #
        #
        return forecast