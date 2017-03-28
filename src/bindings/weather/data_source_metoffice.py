from lists.bindings.list_bindings import get_binding_detail
from index_lists import *
import datetime
import requests


# http://datapoint.metoffice.gov.uk/public/data/
# https://erikflowers.github.io/weather-icons/

BASE_URL = 'http://datapoint.metoffice.gov.uk/public/data/'
URI_LIST_SITE = 'val/wxfcs/all/{datatype}/sitelist'
URI_LIST_REGION = 'txt/wxfcs/regionalforecast/{datatype}/sitelist'
URI_FORECAST_SITE = 'val/wxfcs/all/{datatype}/{locationId}'

LOCATION_id = ''
LOCATION_town = ''
LOCATION_elevation = ''
LOCATION_latitude = ''
LOCATION_longitude = ''
LOCATION_region = ''
LOCATION_unitaryAuthArea = ''
REGION_id = ''


def getParam_unit(params, name):
    for param in params:
        if param['name']==name:
            return param['units']
    return False


def getParam_unit_temp(params, name):
    unit = getParam_unit(params, name)
    if unit == 'C':
        return '&#8451;'
    elif unit == 'F':
        return '&#8457;;'
    else:
        return ''


def _convertMinsToTime(date, mins_from_midnight):
    return datetime.datetime(date.year, date.month, date.day, 0, 0) + datetime.timedelta(minutes=mins_from_midnight)


def createForecast(town):
    #
    getLocation(town)
    #
    forecast_daily = getForcast_daily()
    forecast_3hourly = getForcast_3hourly()
    #
    # Assumption made that where day and night have seperate units defined,
    # these will be the same, therefore taken from day definition
    units_day_json = {}
    units_day_json['weather_type'] = getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'W')
    units_day_json['wind_direction'] = getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'D')
    units_day_json['wind_speed'] = getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'S')
    units_day_json['visibility'] = getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'V')
    units_day_json['temp'] = getParam_unit_temp(forecast_daily['SiteRep']['Wx']['Param'], 'Dm')
    units_day_json['temp_feels'] = getParam_unit_temp(forecast_daily['SiteRep']['Wx']['Param'], 'FDm')
    units_day_json['wind_gust'] = getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'Gn')
    units_day_json['humidity'] = getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'Hn')
    units_day_json['precipitation_prob'] = getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'PPd')
    units_day_json['uv_index'] = getParam_unit(forecast_daily['SiteRep']['Wx']['Param'], 'U')
    #
    units_hour_json = {}
    units_hour_json['weather_type'] = getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'W')
    units_hour_json['wind_direction'] = getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'D')
    units_hour_json['wind_speed'] = getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'S')
    units_hour_json['visibility'] = getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'V')
    units_hour_json['temp'] = getParam_unit_temp(forecast_3hourly['SiteRep']['Wx']['Param'], 'T')
    units_hour_json['temp_feels'] = getParam_unit_temp(forecast_3hourly['SiteRep']['Wx']['Param'], 'F')
    units_hour_json['wind_gust'] = getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'G')
    units_hour_json['humidity'] = getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'H')
    units_hour_json['precipitation_prob'] = getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'Pp')
    units_hour_json['uv_index'] = getParam_unit(forecast_3hourly['SiteRep']['Wx']['Param'], 'U')
    #
    units_json = {}
    units_json['daily'] = units_day_json
    units_json['3hourly'] = units_hour_json
    #
    location_json = {}
    location_json['name'] = LOCATION_town
    location_json['elevation'] = LOCATION_elevation
    location_json['latitude'] = LOCATION_latitude
    location_json['longitude'] = LOCATION_longitude
    location_json['region'] = LOCATION_region
    location_json['unitaryAuthArea'] = LOCATION_unitaryAuthArea
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
                    hr_json_item['time'] = _convertMinsToTime(hour_date, int(rep['$'])).strftime('%H:%M')
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


def getForcast_daily():
    return getForcast('daily')


def getForcast_3hourly():
    return getForcast('3hourly')


def getForcast(frequency):
    # frequency = '3hourly' or 'daily'
    url = '{url}{uri}?res={frequency}&key={key}'.format(url=BASE_URL,
                                                        uri=URI_FORECAST_SITE.format(datatype='json',
                                                                                          locationId=LOCATION_id),
                                                        frequency=frequency,
                                                        key=get_binding_detail('metoffice', 'app_key'))
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return False


def getLocation(town):
    locations = getLocations_list()
    #
    for location in locations:
        if location['name'] == town:
            global LOCATION_town
            LOCATION_town = town
            global LOCATION_id
            LOCATION_id = location['id']
            global LOCATION_elevation
            LOCATION_elevation= location['elevation']
            global LOCATION_latitude
            LOCATION_latitude= location['latitude']
            global LOCATION_longitude
            LOCATION_longitude= location['longitude']
            global LOCATION_region
            LOCATION_region= location['region']
            global LOCATION_unitaryAuthArea
            LOCATION_unitaryAuthArea= location['unitaryAuthArea']


def getLocations_list():
    url = '{url}{uri}?key={key}'.format(url=BASE_URL,
                                        uri=URI_LIST_SITE.format(datatype='json'),
                                        key=get_binding_detail('metoffice', 'app_key'))
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        locations = r.json()
        return locations['Locations']['Location']
    else:
        return False


def getRegion():
    regions = getRegions_list()
    #
    for region in regions:
        if region['@name'] == LOCATION_region:
            global REGION_id
            REGION_id = region['@id']


def getRegions_list():
    url = '{url}{uri}?key={key}'.format(url=BASE_URL,
                                        uri=URI_LIST_REGION.format(datatype='json'),
                                        key=get_binding_detail('metoffice', 'app_key'))
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        locations = r.json()
        return locations['Locations']['Location']
    else:
        return False
