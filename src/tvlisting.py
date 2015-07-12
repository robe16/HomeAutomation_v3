from datetime import datetime, timedelta
from enum_tvlistings import enum_channels
import cmd_http


def getalllistings():
    channels = enum_channels.LSTchannels
    x=0
    while x<len(channels):
        channels[x].append(getlistings(channels[x][2]))
        x+=1
    return channels


def getlistings(RTchannelID):
    x = cmd_http.sendHTTP("http://xmltv.radiotimes.com/xmltv/%s.dat" % (RTchannelID), "close")
    if not x==False:
        x = x.read()
        return sortlistings(x)
    else:
        return ["--"]


def sortlistings(result):

    ARRresultlines = filter(None, result.split('\n'))

    count=2
    while count<max(ARRresultlines):
        resultbreakdown = ARRresultlines[count].split('~')
        #String date will be in format "dd/MM/yyyy HH:mm"
        DATETIMEstart = datetime.strptime(resultbreakdown[19]+" "+resultbreakdown[20], '%d/%m/%Y %H:%M')
        DATETIMEend = datetime.strptime(resultbreakdown[19]+" "+resultbreakdown[21], '%d/%m/%Y %H:%M')

        if not DATETIMEstart <= DATETIMEend:
            DATETIMEend = DATETIMEend + timedelta(days=1)

        if DATETIMEstart<=datetime.now() and DATETIMEend>=datetime.now():
            #
            response=[]
            response.append([DATETIMEstart, DATETIMEend, resultbreakdown[0], resultbreakdown[17]])
            #now get next listed item
            next=1
            while next<=5:
                resultbreakdown = ARRresultlines[count+next].split('~')
                DATETIMEstart = datetime.strptime(resultbreakdown[19]+" "+resultbreakdown[20], '%d/%m/%Y %H:%M')
                DATETIMEend = datetime.strptime(resultbreakdown[19]+" "+resultbreakdown[21], '%d/%m/%Y %H:%M')
                response.append([DATETIMEstart, DATETIMEend, resultbreakdown[0], resultbreakdown[17]])
                next+=1
            return response

        count+=1

    return False