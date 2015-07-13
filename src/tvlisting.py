from datetime import datetime, timedelta
from enum_tvlistings import enum_channels
import cmd_http


def getalllistings():
    channels = enum_channels.LSTchannels
    STRxml = "<listings>"
    x=0
    while x<len(channels):
        STRxml+= getlistings(channels[x], x)
        x+=1
        print ("%s out of %s completed" % (x, len(channels)))
    STRxml += "</listings>"
    return STRxml


def getlistings(LSTchanneldetails, id):
    x = cmd_http.sendHTTP("http://xmltv.radiotimes.com/xmltv/%s.dat" % (LSTchanneldetails[2]), "close")
    STRxml = "<channel id=\"%s\"><details><tivo>%s</tivo><name>%s</name></details>" % (id, str(LSTchanneldetails[0]), str(LSTchanneldetails[1]))
    if not x==False:
        x = x.read()
        STRxml += sortlistings(x)
    else:
        STRxml += "<listing>--</listing>"
    STRxml += "</channel>"
    return STRxml


def sortlistings(result):

    ARRresultlines = filter(None, result.split('\n'))

    count=2
    while count<max(ARRresultlines):
        resultbreakdown = ARRresultlines[count].split('~')
        # String date will be in format "dd/MM/yyyy HH:mm"
        DATETIMEstart = datetime.strptime(resultbreakdown[19]+" "+resultbreakdown[20], '%d/%m/%Y %H:%M')
        DATETIMEend = datetime.strptime(resultbreakdown[19]+" "+resultbreakdown[21], '%d/%m/%Y %H:%M')

        if not DATETIMEstart <= DATETIMEend:
            DATETIMEend = DATETIMEend + timedelta(days=1)

        if DATETIMEstart<=datetime.now() and DATETIMEend>=datetime.now():
            #
            STRxml = ""
            next=0
            while next<=5:
                resultbreakdown = ARRresultlines[count+next].split('~')
                STRxml += "<listing><start>%s</start><end>%s</end><name>%s</name><blurb>%s</blurb></listing>" % (resultbreakdown[19]+" "+resultbreakdown[20], resultbreakdown[19]+" "+resultbreakdown[21], resultbreakdown[0], resultbreakdown[17])
                next+=1
            #
            return STRxml
        count+=1

    return "<listing>--</listing>"