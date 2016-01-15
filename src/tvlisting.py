from datetime import datetime, timedelta
import json
import os
from send_cmds import sendHTTP
from object_channel import object_channel


def build_channel_array():
    with open(os.path.join('lists', 'list_channels.json'), 'r') as data_file:
        data = json.load(data_file)
    data_channels = data["channels"]
    #
    list_channels = []
    x = 0
    while x < len(data_channels):
        #
        chan = data_channels[x]
        #
        print (
            'Building channels and retrieving TV Listing information: {current} out of {total} - {name}'.format(current = x + 1,
                                                                                                                total = len(data_channels),
                                                                                                                name = chan['name']))
        #
        dict_devicekeys = {}
        for k, v in chan['devicekeys'].items():
            dict_devicekeys[k] = v
        #
        dict_listingsrc = {}
        dict_listings = {}
        for k, v in chan['listingsrc'].items():
            dict_listingsrc[k] = v
            dict_listings[k] = getlisting(k, v)
        #
        objchan = object_channel(chan['name'], chan['logo'], chan['type'], chan['enabled'],
                                 dict_devicekeys, dict_listingsrc, dict_listings, datetime.now())
        #
        list_channels.append(objchan)
        #
        x += 1
        #
    return list_channels


def getlisting(src, value):
    if src == 'radiotimes':
        x = sendHTTP('http://xmltv.radiotimes.com/xmltv/{code}.dat'.format(code = value), "close")
        data = x.read() if bool(x) else None
    else:
        data = None
    return data


def returnnownext(src, data):
    if src == 'radiotimes':
        arr_data_alllines = filter(None, data.split('\n'))
        count = 2
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


def returnnonext_xml_all(dict_channels, chan=None):
    str_xml = '<timestamp>{}</timestamp>'.format(datetime.now().strftime('%d/%m/%Y %H:%M'))
    if chan:
        str_xml += returnnownext_xml(dict_channels[chan])
    else:
        for chan in dict_channels.items():
            str_xml += returnnownext_xml(dict_channels[chan])
    return str_xml


def returnnownext_xml(objchan):
    str_xml = '<channel><details><name>{}</name><logo>{}</logo><type>{}</type></details>'.format(id, objchan.name(),
                                                                                                 objchan.logo(),
                                                                                                 objchan.type())
    if not objchan.getListings() == None:
        for src, data in objchan.getListings().items():
            if data:
                dict_nownextlisting = returnnownext(src, data)
                for dict_listing in dict_nownextlisting.items():
                    str_xml += '<listing><start>{}</start><end>{}</end><name>{}</name><desc>{}</desc></listing>'.format(
                        dict_listing['startdate'] + " " + dict_listing['starttime'],
                        dict_listing['enddate'] + " " + dict_listing['endtime'], dict_listing['title'],
                        dict_listing['desc'])
                str_xml += '</channel>'
                return str_xml
    str_xml += '<listing>--</listing></channel>'
    return str_xml
# <listingtimestamp>{}</listingtimestamp>