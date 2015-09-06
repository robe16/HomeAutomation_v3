from datetime import datetime, timedelta
import enum_channels
import send_cmds


def getall_listings():
    channels = enum_channels.LSTchannels
    x = 0
    while x < len(channels):
        print ('Retrieving TV Listing information: {} out of {} completed - {}'.format(x + 1, len(channels), channels[x][0]))
        channels[x].append(get_listings(channels[x]))
        x += 1
    return [channels, datetime.now()]


def get_listings(list_channeldetails):
    x = send_cmds.sendHTTP('http://xmltv.radiotimes.com/xmltv/{}.dat'.format(list_channeldetails[1]), "close")
    return x.read() if not bool(x) else None


def getall_xmllistings(data):
    str_xml = '<listings><timestamp>{}</timestamp>'.format(datetime.now().strftime('%d/%m/%Y %H:%M'))
    x = 0
    while x < len(data):
        str_xml += get_xmllistings(data[x], x)
        x += 1
    str_xml += "</listings>"
    return str_xml


def get_xmllistings(data, id):
    str_xml = '<channel id="{}"><details><name>{}</name><logo>{}</logo><type>{}</type><tivo>{}</tivo></details>'.format(id, str(data[0]), str(data[2]), str(data[3]), str(data[4]))
    if not data[5] == False and not data[5] == None:
        str_xml += sort_xmllistings(data[5])
    else:
        str_xml += "<listing>--</listing>"
    str_xml += "</channel>"
    return str_xml


def sort_xmllistings(result):
    arr_resultlines = filter(None, result.split('\n'))

    count = 2
    while count < len(arr_resultlines):
        resultbreakdown = arr_resultlines[count].split('~')
        # String date will be in format "dd/MM/yyyy HH:mm"
        datetime_start = datetime.strptime(resultbreakdown[19] + " " + resultbreakdown[20], '%d/%m/%Y %H:%M')
        datetime_end = datetime.strptime(resultbreakdown[19] + " " + resultbreakdown[21], '%d/%m/%Y %H:%M')

        if not datetime_start <= datetime_end:
            datetime_end = datetime_end + timedelta(days=1)

        if datetime_start <= datetime.now() <= datetime_end:
            #
            str_xml = ""
            next = 0
            while next <= 5:
                resultbreakdown = arr_resultlines[count + next].split('~')
                datetime_start = datetime.strptime(resultbreakdown[19] + " " + resultbreakdown[20], '%d/%m/%Y %H:%M')
                datetime_end = datetime.strptime(resultbreakdown[19] + " " + resultbreakdown[21], '%d/%m/%Y %H:%M')
                if not datetime_start <= datetime_end:
                    datetime_end = datetime_end + timedelta(days=1)
                str_xml += '<listing><start>{}</start><end>{}</end><name>{}</name><blurb>{}</blurb></listing>'.format(datetime_start.strftime('%d/%m/%Y %H:%M'), datetime_end.strftime('%d/%m/%Y %H:%M'), resultbreakdown[0], resultbreakdown[17])
                next += 1
            #
            return str_xml
        count += 1

    return "<listing>--</listing>"


def sort_arrlistings(result):
    arr_resultlines = filter(None, result.split('\n'))

    count = 2
    while count < max(arr_resultlines):
        resultbreakdown = arr_resultlines[count].split('~')
        # String date will be in format "dd/MM/yyyy HH:mm"
        datetime_start = datetime.strptime(resultbreakdown[19] + " " + resultbreakdown[20], '%d/%m/%Y %H:%M')
        datetime_end = datetime.strptime(resultbreakdown[19] + " " + resultbreakdown[21], '%d/%m/%Y %H:%M')

        if not datetime_start <= datetime_end:
            datetime_end = datetime_end + timedelta(days=1)

        if datetime_start <= datetime.now() <= datetime_end:
            #
            arr_listing = [[datetime_start.strftime('%d/%m/%Y'),
                           datetime_start.strftime('%H:%M'),
                           datetime_end.strftime('%d/%m/%Y'),
                           datetime_end.strftime('%H:%M'),
                           resultbreakdown[0],
                           resultbreakdown[17]]]
            next = 1
            while next <= 5:
                resultbreakdown = arr_resultlines[count + next].split('~')
                datetime_start = datetime.strptime(resultbreakdown[19] + " " + resultbreakdown[20], '%d/%m/%Y %H:%M')
                datetime_end = datetime.strptime(resultbreakdown[19] + " " + resultbreakdown[21], '%d/%m/%Y %H:%M')
                if not datetime_start <= datetime_end:
                    datetime_end = datetime_end + timedelta(days=1)
                arr_listing.append([datetime_start.strftime('%d/%m/%Y'),
                                   datetime_start.strftime('%H:%M'),
                                   datetime_end.strftime('%d/%m/%Y'),
                                   datetime_end.strftime('%H:%M'),
                                   resultbreakdown[0],
                                   resultbreakdown[17]])
                next += 1
            #
            return arr_listing
        count += 1
    return False
