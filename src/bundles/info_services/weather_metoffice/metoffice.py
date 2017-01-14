from bundles.info_services.info_service import InfoService
from config.bundles.config_bundles import get_cfg_structure_town
from index_lists import *
from log.console_messages import print_error
import datetime
import requests


class info_metoffice(InfoService):

    # http://datapoint.metoffice.gov.uk/public/data/
    # https://erikflowers.github.io/weather-icons/

    APP_KEY = '186ae211-9495-4a9b-8a15-6b8d6140dfa6'
    BASE_URL = 'http://datapoint.metoffice.gov.uk/public/data/'
    URI_LIST_SITE = 'val/wxfcs/all/{datatype}/sitelist'
    URI_LIST_REGION = 'txt/wxfcs/regionalforecast/{datatype}/sitelist'
    URI_FORECAST_SITE = 'val/wxfcs/all/{datatype}/{locationId}'

    LOCATION_id = ''
    LOCATION_elevation = ''
    LOCATION_latitude = ''
    LOCATION_longitude = ''
    LOCATION_region = ''
    LOCATION_unitaryAuthArea = ''
    REGION_id = ''

    def __init__ (self):
        #
        InfoService.__init__(self, 'metoffice')
        #
        self.getLocation()

    def getData(self, request):
        try:
            if request['data'] == 'forecast':
                return self.createForecast()
        except Exception as e:
            print_error('Failed to return requested data {request} - {error}'.format(request=request['data'],
                                                                                     error=e))
            return False

    def getParam_unit(self, params, name):
        for param in params:
            if param['name']==name:
                return param['units']
        return False

    def getParam_unit_temp(self, params, name):
        unit = self.getParam_unit(params, name)
        if unit == 'C':
            return '&#8451;'
        elif unit == 'F':
            return '&#8457;;'
        else:
            return ''

    def _convertMinsToTime(self, date, mins_from_midnight):
        return datetime.datetime(date.year, date.month, date.day, 0, 0) + datetime.timedelta(minutes=mins_from_midnight)

    def createForecast(self):
        #
        forecast_daily = self.getForcast_daily()
        forecast_3hourly = self.getForcast_3hourly()
        #
        # Assumption made that where day and night have seperate units defined,
        # these will be the same, therefore taken from day definition
        units_day_json = {}
        units_day_json['weather_type'] = self.getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'W')
        units_day_json['wind_direction'] = self.getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'D')
        units_day_json['wind_speed'] = self.getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'S')
        units_day_json['visibility'] = self.getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'V')
        units_day_json['temp'] = self.getParam_unit_temp(forecast_daily['SiteRep']['Wx']['Param'], 'Dm')
        units_day_json['temp_feels'] = self.getParam_unit_temp(forecast_daily['SiteRep']['Wx']['Param'], 'FDm')
        units_day_json['wind_gust'] = self.getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'Gn')
        units_day_json['humidity'] = self.getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'Hn')
        units_day_json['precipitation_prob'] = self.getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'PPd')
        units_day_json['uv_index'] = self.getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'U')
        #
        units_hour_json = {}
        units_hour_json['weather_type'] = self.getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'W')
        units_hour_json['wind_direction'] = self.getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'D')
        units_hour_json['wind_speed'] = self.getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'S')
        units_hour_json['visibility'] = self.getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'V')
        units_hour_json['temp'] = self.getParam_unit_temp(forecast_3hourly['SiteRep']['Wx']['Param'], 'T')
        units_hour_json['temp_feels'] = self.getParam_unit_temp(forecast_3hourly['SiteRep']['Wx']['Param'], 'F')
        units_hour_json['wind_gust'] = self.getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'G')
        units_hour_json['humidity'] = self.getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'H')
        units_hour_json['precipitation_prob'] = self.getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'Pp')
        units_hour_json['uv_index'] = self.getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'U')
        #
        units_json = {}
        units_json['daily'] = units_day_json
        units_json['3hourly'] = units_hour_json
        #
        location_json = {}
        location_json['name'] = get_cfg_structure_town()
        location_json['elevation'] = self.LOCATION_elevation
        location_json['latitude'] = self.LOCATION_latitude
        location_json['longitude'] = self.LOCATION_longitude
        location_json['region'] = self.LOCATION_region
        location_json['unitaryAuthArea'] = self.LOCATION_unitaryAuthArea
        #
        jsonForecast = {}
        jsonForecast['units'] = units_json
        jsonForecast['location'] = location_json
        jsonForecast['days'] = {}
        #
        dy_count = 0
        #
        for day_period in forecast_daily['SiteRep']['DV']['Location']['Period']:
            #
            date_json = {}
            #
            # date held in format '2012-11-21Z'
            dy_date = datetime.datetime.strptime(day_period['value'].replace('Z', ''), "%Y-%m-%d")
            dy_date_str = day_period['value'].replace('Z', '')
            #
            day_json = {}
            night_json = {}
            #
            for rep in day_period['Rep']:
                #
                if rep['$'] == 'Day':
                    #
                    day_json['weather_type'] = str(rep['W'])
                    day_json['wind_direction'] = rep['D']
                    day_json['wind_speed'] = rep['S']
                    day_json['visibility'] = getVisibility_desc(rep['V'])
                    day_json['temp'] = rep['Dm']
                    day_json['temp_feels'] = rep['FDm']
                    day_json['wind_gust'] = rep['Gn']
                    day_json['humidity'] = rep['Hn']
                    day_json['precipitation_prob'] = rep['PPd']
                    day_json['uv_index'] = getUV_desc(int(rep['U']))
                    #
                else:
                    #
                    night_json['weather_type'] = str(rep['W'])
                    night_json['wind_direction'] = rep['D']
                    night_json['wind_speed'] = rep['S']
                    night_json['visibility'] = getVisibility_desc(rep['V'])
                    night_json['temp'] = rep['Nm']
                    night_json['temp_feels'] = rep['FNm']
                    night_json['wind_gust'] = rep['Gm']
                    night_json['humidity'] = rep['Hm']
                    night_json['precipitation_prob'] = rep['PPn']
                    night_json['uv_index'] = '-'
                    #
                #
            hourly_json = {}
            #
            for hour_period in forecast_3hourly['SiteRep']['DV']['Location']['Period']:
                #
                hour_date = datetime.datetime.strptime(hour_period['value'].replace('Z', ''), "%Y-%m-%d")
                hr_date_str = hour_period['value'].replace('Z', '')
                #
                if hr_date_str == dy_date_str:
                    #
                    hourly_json = {}
                    hr_count = 0
                    #
                    for rep in hour_period['Rep']:
                        #
                        hr_json_item = {}
                        hr_json_item['time'] = self._convertMinsToTime(hour_date, int(rep['$'])).strftime('%H:%M')
                        hr_json_item['weather_type'] = str(rep['W'])
                        hr_json_item['wind_direction'] = rep['D']
                        hr_json_item['wind_speed'] = rep['S']
                        hr_json_item['visibility'] = getVisibility_desc(rep['V'])
                        hr_json_item['temp'] = rep['T']
                        hr_json_item['temp_feels'] = rep['F']
                        hr_json_item['wind_gust'] = rep['G']
                        hr_json_item['humidity'] = rep['H']
                        hr_json_item['precipitation_prob'] = rep['Pp']
                        hr_json_item['uv_index'] = getUV_desc(int(rep['U']))
                        #
                        hourly_json[hr_count] = hr_json_item
                        #
                        hr_count += 1
                        #
            #
            date_json['date'] = dy_date_str
            date_json['daytime'] = day_json
            date_json['nighttime'] = night_json
            date_json['3hourly'] = hourly_json
            #
            jsonForecast['days'][dy_count] = date_json
            #
            dy_count += 1
        #
        return jsonForecast

    def getForcast_daily(self):
        return self.getForcast('daily')

    def getForcast_3hourly(self):
        return self.getForcast('3hourly')

    def getForcast(self, frequency):
        # frequency = '3hourly' or 'daily'
        url = '{url}{uri}?res={frequency}&key={key}'.format(url=self.BASE_URL,
                                                            uri=self.URI_FORECAST_SITE.format(datatype='json',
                                                                                              locationId=self.LOCATION_id),
                                                            frequency=frequency,
                                                            key=self.APP_KEY)
        r = requests.get(url)
        #
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            return False

    def getLocation(self):
        locations = self.getLocations_list()
        config_town = get_cfg_structure_town()
        #
        for location in locations:
            if location['name'] == config_town:
                self.LOCATION_id = location['id']
                self.LOCATION_elevation = location['elevation']
                self.LOCATION_latitude = location['latitude']
                self.LOCATION_longitude = location['longitude']
                self.LOCATION_region = location['region']
                self.LOCATION_unitaryAuthArea = location['unitaryAuthArea']

    def getLocations_list(self):
        url = '{url}{uri}?key={key}'.format(url=self.BASE_URL,
                                            uri=self.URI_LIST_SITE.format(datatype='json'),
                                            key=self.APP_KEY)
        r = requests.get(url)
        #
        if r.status_code == requests.codes.ok:
            locations = r.json()
            return locations['Locations']['Location']
        else:
            return False

    def getRegion(self):
        regions = self.getRegions_list()
        #
        for region in regions:
            if region['@name'] == self.LOCATION_region:
                self.REGION_id = region['@id']

    def getRegions_list(self):
        url = '{url}{uri}?key={key}'.format(url=self.BASE_URL,
                                            uri=self.URI_LIST_REGION.format(datatype='json'),
                                            key=self.APP_KEY)
        r = requests.get(url)
        #
        if r.status_code == requests.codes.ok:
            locations = r.json()
            return locations['Locations']['Location']
        else:
            return False