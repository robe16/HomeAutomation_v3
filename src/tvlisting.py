from datetime import datetime, timedelta
import json
import os
from object_channel import object_channel
from console_messages import print_channelbuild, print_msg
import tvlisting_radiotimes


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
                temp_listing = getlisting(k, v)
                if temp_listing != None:
                    dict_listings[k] = getlisting(k, v)
                    break
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
    if value != '':
        if src == 'radiotimes':
            return tvlisting_radiotimes.getlisting(value)
        else:
            print_msg('No known listing source available')
    else:
        print_msg('No code provided for listing source ' + src)
    return None


def returnnownext(src, data):
    if src == 'radiotimes':
        return tvlisting_radiotimes.nownext(data)
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