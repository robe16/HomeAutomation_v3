from datetime import datetime, timedelta
import enum_channels
import send_cmds


def getall_listings():
    channels = enum_channels.LSTchannels
    x=0
    while x<len(channels):
        print ("Retrieving TV Listing information: %s out of %s completed - %s" % (x+1, len(channels), channels[x][0]))
        channels[x].append(get_listings(channels[x]))
        x+=1
    return [channels, datetime.now()]

def get_listings(LSTchanneldetails):
    x = send_cmds.sendHTTP("http://xmltv.radiotimes.com/xmltv/%s.dat" % (LSTchanneldetails[1]), "close")
    if not x==False:
        return x.read()
    else:
        return None


def getall_xmllistings(data):
    STRxml = "<listings><timestamp>%s</timestamp>" % (datetime.now().strftime('%d/%m/%Y %H:%M'))
    x=0
    while x<len(data):
        STRxml+= get_xmllistings(x, data[x])
        x+=1
    STRxml += "</listings>"
    return STRxml

def get_xmllistings(id, data):
    STRxml = "<channel id=\"%s\"><details><name>%s</name><logo>%s</logo><type>%s</type><tivo>%s</tivo></details>" % (id, str(data[0]), str(data[2]), str(data[3]), str(data[4]))
    if not data[5]==False and not data[5]==None:
        STRxml += XMLsortlistings(data[5])
    else:
        STRxml += "<listing>--</listing>"
    STRxml += "</channel>"
    return STRxml


def XMLsortlistings(result):

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
                DATETIMEstart = datetime.strptime(resultbreakdown[19]+" "+resultbreakdown[20], '%d/%m/%Y %H:%M')
                DATETIMEend = datetime.strptime(resultbreakdown[19]+" "+resultbreakdown[21], '%d/%m/%Y %H:%M')
                if not DATETIMEstart <= DATETIMEend:
                    DATETIMEend = DATETIMEend + timedelta(days=1)
                STRxml += "<listing><start>%s</start><end>%s</end><name>%s</name><blurb>%s</blurb></listing>" % (DATETIMEstart.strftime('%d/%m/%Y %H:%M'), DATETIMEend.strftime('%d/%m/%Y %H:%M'), resultbreakdown[0], resultbreakdown[17])
                next+=1
            #
            return STRxml
        count+=1

    return "<listing>--</listing>"


def ARRsortlistings(result):

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
            ARRlisting = [[DATETIMEstart.strftime('%d/%m/%Y'),
                           DATETIMEend.strftime('%H:%M'),
                           DATETIMEstart.strftime('%d/%m/%Y'),
                           DATETIMEend.strftime('%H:%M'),
                           resultbreakdown[0],
                           resultbreakdown[17]]]
            next=1
            while next<=5:
                resultbreakdown = ARRresultlines[count+next].split('~')
                DATETIMEstart = datetime.strptime(resultbreakdown[19]+" "+resultbreakdown[20], '%d/%m/%Y %H:%M')
                DATETIMEend = datetime.strptime(resultbreakdown[19]+" "+resultbreakdown[21], '%d/%m/%Y %H:%M')
                if not DATETIMEstart <= DATETIMEend:
                    DATETIMEend = DATETIMEend + timedelta(days=1)
                ARRlisting.append([DATETIMEstart.strftime('%d/%m/%Y'),
                                   DATETIMEstart.strftime('%H:%M'),
                                   DATETIMEend.strftime('%d/%m/%Y'),
                                   DATETIMEend.strftime('%H:%M'),
                                   resultbreakdown[0],
                                   resultbreakdown[17]])
                next+=1
            #
            return ARRlisting
        count+=1
    return False