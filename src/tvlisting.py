from datetime import datetime, timedelta
import json
import os
from send_cmds import sendHTTP
from object_channel import object_channel
from console_messages import print_channelbuild


def build_channel_array():
    with open(os.path.join('lists', 'list_channels.json'), 'r') as data_file:
        data = json.load(data_file)
    #
    list_channels = {'categories': data['categories']}
    list_channels['channels'] = {}
    #
    data_channels = data["channels"]
    #
    # Count number of channels in total
    total = 0
    for cat in data['categories']:
        total += len(data_channels[cat])
    #
    x = 0
    for cat in data['categories']:
        cat_channels = []
        data_categories = data_channels[cat]
        for chan in data_categories:
            #
            x += 1
            #
            print_channelbuild(x, total, chan['name'])
            #
            # Listing sources
            dict_listingsrc = {}
            dict_listings = {}
            for k, v in chan['listingsrc'].items():
                dict_listingsrc[k] = v
                dict_listings[k] = getlisting(k, v)
            #
            # Compile into object
            objchan = object_channel(chan['name'],
                                     cat,
                                     dict_listingsrc,
                                     dict_listings,
                                     datetime.now())
            #
            cat_channels.append(objchan)
            #
        list_channels['channels'][cat] = cat_channels
        #
    return list_channels


def getlisting(src, value):
    if src == 'radiotimes' and value != '':
        x = sendHTTP('http://xmltv.radiotimes.com/xmltv/{code}.dat'.format(code = value), 'close', contenttype='text/xml; charset=utf-8')
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