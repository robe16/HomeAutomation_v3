from bundles.info_services.info_service import InfoService
from log.console_messages import print_error
import json
from data_source_metoffice import createForecast
from data_source_sunrise_sunset_org import createSunriseSet


class info_metoffice(InfoService):

    def __init__ (self):
        #
        InfoService.__init__(self, 'metoffice')

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
        forecast = createForecast()
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