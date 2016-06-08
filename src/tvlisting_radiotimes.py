from datetime import datetime, timedelta
from send_cmds import sendHTTP


def getlisting(value):
    x = sendHTTP('http://xmltv.radiotimes.com/xmltv/{code}.dat'.format(code=value), 'close',
                 contenttype='text/xml; charset=utf-8')
    return x.read() if bool(x) else None

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