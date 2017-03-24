from config.bindings.config_bindings import get_cfg_structure_town
from index_lists import *
import datetime
import requests


# http://http://sunrise-sunset.org/api

BASE_URL = 'http://api.sunrise-sunset.org/json'
QUERY_REQUEST = '?lat={lat}&lng={lng}&date={date}&formatted=0'


def _convertMinsToTime(date, mins_from_midnight):
    return datetime.datetime(date.year, date.month, date.day, 0, 0) + datetime.timedelta(minutes=mins_from_midnight)


def createSunriseSet(date, latitude, longitude):
    #
    jsonSunRiseSet = {}
    #
    jsonResponse = getSunRiseSet(date, latitude, longitude)
    #
    if jsonResponse['status']=='OK':
        sunrise = convertISOdateResponse(jsonResponse['results']['sunrise'])
        sunset = convertISOdateResponse(jsonResponse['results']['sunset'])
        #
        jsonSunRiseSet = {'sunrise': sunrise.isoformat(' '),
                          'sunset': sunset.isoformat(' ')}
    #
    return jsonSunRiseSet


def getSunRiseSet(date, latitude, longitude):
    url = '{url}{uri}'.format(url=BASE_URL,
                              uri=QUERY_REQUEST.format(lat=latitude,
                                                       lng=longitude,
                                                       date=date))
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return {'status': 'ERROR'}


def convertISOdateResponse(date_string):
    #2015-05-21T05:05:35+00:00
    ret = datetime.datetime.strptime(date_string[:19], '%Y-%m-%dT%H:%M:%S')
    if date_string[19] == '+':
        ret -= datetime.timedelta(hours=int(date_string[20:22]), minutes=int(date_string[23:]))
    elif date_string[19] == '-':
        ret += datetime.timedelta(hours=int(date_string[20:22]), minutes=int(date_string[23:]))
    return ret