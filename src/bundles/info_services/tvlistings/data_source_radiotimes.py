from datetime import datetime, timedelta
import requests as requests

################################################################
################################################################
# Code will no longer work following the
# decommission of the Radiotimes API
################################################################
################################################################

def get(channel_id):
    #
    str_listing = getlisting(channel_id)
    #
    dict_listing = {}
    dict_listing['enabled'] = True
    dict_listing['listings'] = convert_to_dict(str_listing)
    #
    return dict_listing


def convert_to_dict(data):
    arr_data_alllines = filter(None, data.split('\n'))
    #
    json_channel = {}
    #
    count = 4
    while count < max(arr_data_alllines):
        arr_data_oneline = arr_data_alllines[count].split('~')
        json_programme = {}
        #
        datetime_start = datetime.strptime(arr_data_oneline[19] + " " + arr_data_oneline[20], '%d/%m/%Y %H:%M')
        datetime_end = datetime.strptime(arr_data_oneline[19] + " " + arr_data_oneline[21], '%d/%m/%Y %H:%M')
        #
        if not datetime_start <= datetime_end:
            datetime_end = datetime_end + timedelta(days=1)
        #
        json_programme['start'] = datetime_start
        json_programme['end'] = datetime_end
        json_programme['title'] = arr_data_oneline[0]
        json_programme['subtitle'] = ''
        json_programme['desc'] = arr_data_oneline[17]
        #
        id = json_programme['start'].isoformat(' ')
        json_channel[id] = json_programme
        #
        count += 1
        #
    return json_channel


def getlisting(channel_id):
    #
    headers = {'Connection': 'close',
               'content-type': 'text/xml; charset=utf-8'}
    #
    r = requests.get('http://xmltv.radiotimes.com/xmltv/{channel_id}.dat'.format(channel_id=channel_id),
                     headers=headers)
    #
    if r.status_code == requests.codes.ok:
        return r.content
    else:
        return None


# Legacy code below from old instance of server

def nownext(data):
    arr_data_alllines = filter(None, data.split('\n'))
    count = 4
    while count < max(arr_data_alllines):
        arr_data_oneline = arr_data_alllines[count].split('~')
        # String date will be in format "dd/MM/yyyy HH:mm"
        datetime_start = datetime.strptime(arr_data_oneline[19] + " " + arr_data_oneline[20], '%d/%m/%Y %H:%M')
        datetime_end = datetime.strptime(arr_data_oneline[19] + " " + arr_data_oneline[21], '%d/%m/%Y %H:%M')

        if not datetime_start <= datetime_end:
            datetime_end = datetime_end + timedelta(days=1)

        if datetime_start <= datetime.now() <= datetime_end:
            #
            dict_nownext = {}
            next = 0
            while next <= 5:
                arr_data_oneline = arr_data_alllines[count + next].split('~')
                datetime_start = datetime.strptime(arr_data_oneline[19] + " " + arr_data_oneline[20],
                                                   '%d/%m/%Y %H:%M')
                datetime_end = datetime.strptime(arr_data_oneline[19] + " " + arr_data_oneline[21],
                                                 '%d/%m/%Y %H:%M')
                if not datetime_start <= datetime_end:
                    datetime_end = datetime_end + timedelta(days=1)
                #
                dict_listing = {}
                dict_listing['startdate'] = datetime_start.strftime('%d/%m/%Y')
                dict_listing['starttime'] = datetime_start.strftime('%H:%M')
                dict_listing['enddate'] = datetime_end.strftime('%d/%m/%Y')
                dict_listing['endtime'] = datetime_end.strftime('%H:%M')
                dict_listing['title'] = arr_data_oneline[0]
                dict_listing['desc'] = arr_data_oneline[17]
                #
                dict_nownext[next] = dict_listing
                #
                next += 1
            #
            return dict_nownext
        count += 1
    return None