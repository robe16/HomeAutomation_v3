import dataholder
from config import read_config, write_config
import create_objects
from object_tv_lg import object_LGTV
from object_tivo import object_TIVO
from web_createpages import create_home, create_loungetv, create_tvguide, create_settings, create_about
import os, time
from tvlisting import getall_listings, getall_xmllistings, get_xmllistings
from bottle import route, request, run, static_file, HTTPResponse, template, redirect
from multiprocessing import Process, Queue
import string
import random

def start_bottle():
    run(host='0.0.0.0', port=1616, debug=True) # '0.0.0.0' will listen on all interfaces including the external one
    #run(host='localhost', port=8080, debug=True)

def server_start():
    tvlistings_startprocess()
    p2.start()

def server_end():
    p1.terminate()
    p2.terminate()

def tvlistings_startprocess():
    p1.start()

def tvlistings_process(LSTlistings):
    # 604800 secs = 7 days
    while True:
        LSTlistings.put(getall_listings())
        time.sleep(604800)

@route('/')
def web_redirect():
    redirect("/web/home")

@route('/web/<page>')
def web(page=""):
    if not LSTlistings.empty():
        temp = LSTlistings.get()
        LSTlistings.put(temp)
        listings=temp[0]
    else:
        listings = False
    if page=="home":
        return HTTPResponse(body=create_home(), status=200)
    elif page=="loungetv":
        return HTTPResponse(body=create_loungetv(listings), status=200)
    elif page=="tvguide":
        return HTTPResponse(body=create_tvguide(listings), status=200)
    elif page=="settings":
        return HTTPResponse(body=create_settings(dataholder.STRnest_clientID, dataholder.STRnest_pincode, dataholder.randomstring), status=200)
    elif page=="about":
        return HTTPResponse(body=create_about(), status=200)
    else:
        return HTTPResponse(body="An error has occurred", status=400)

@route('/web/static/<folder>/<filename>')
def get_image(folder, filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__), ('web/static/%s' % folder)))

@route('/device/<room>/<device>/<command>')
def send_command(room="-", device="-", command="-"):
    if room=="lounge" and device=="lgtv" and command=="appslist":
        APPtype = request.query.type or 3
        APPindex = request.query.index or 0
        APPnumber = request.query.number or 0
        x = dataholder.OBJloungetv.getApplist(APPtype=APPtype, APPindex=APPindex, APPnumber=APPnumber)
        return HTTPResponse(body=x, status=200) if bool(x) else HTTPResponse(status=400)
    elif room=="lounge" and device=="lgtv" and command=="appicon":
        auid = request.query.auid or False
        name = request.query.name or False
        if not bool(auid) or not bool(name):
            return HTTPResponse(status=400)
        x = dataholder.OBJloungetv.getAppicon(auid, name)
        return HTTPResponse(body=x, status=200, content_type='image/png') if bool(x) else HTTPResponse(status=400)
    # TV Command
    elif room=="lounge" and device=="lgtv":
        return HTTPResponse(status=200) if dataholder.OBJloungetv.sendCmd(command) else HTTPResponse(status=400)
    # TiVo Command
    elif room=="lounge" and device=="tivo":
        if command=="channel":
            channo = request.query.id or False
            print request.query.id
            if channo:
                return HTTPResponse(status=200) if dataholder.OBJloungetivo.sendCmd(("FORCECH {}\r").format(channo)) else HTTPResponse(status=400)
            else:
                HTTPResponse(status=400)
        else:
            return HTTPResponse(status=200) if dataholder.OBJloungetivo.sendCmd(command) else HTTPResponse(status=400)
    else:
        return HTTPResponse(status=400)

@route('/tvlistings')
def get_tvlistings():
    if not LSTlistings.get()[0]:
        return HTTPResponse(status=400)
    channel = request.query.id or False
    x = get_xmllistings(LSTlistings.get()[0]) if bool(channel) else getall_xmllistings(LSTlistings.get()[0])
    return HTTPResponse(body=x, status=200) if bool(x) else HTTPResponse(status=400)

@route('/settings/<x>')
def save_settings(x="-"):
    if x=="nest":
        pincode = request.query.pincode
        if not bool(pincode):
            return HTTPResponse(status=400)
        dataholder.STRnest_pincode = pincode
        write_config()
        return HTTPResponse(status=200)
    else:
        return HTTPResponse(status=400)

@route('/favicon.ico')
def send_favicon():
    return HTTPResponse(status=400)
    #root = os.path.join(os.path.dirname(__file__), '..', 'img/favicon.ico')
    #return static_file(filename, root=root)

@route('/img/<category>/<filename:re:.*\.png>')
def get_image(category, filename):
    root = os.path.join(os.path.dirname(__file__), '..', 'img/%s' % category)
    return static_file(filename, root=root, mimetype='image/png')


# Get configuration
read_config()
# Create objects
dataholder.randomstring = (''.join(random.choice(string.ascii_lowercase) for i in range(5)))
dataholder.OBJloungetv = create_objects.create_lgtv(dataholder.STRloungetv_lgtv_ipaddress,dataholder.STRloungetv_lgtv_pairkey)
dataholder.OBJloungetivo = create_objects.create_tivo(dataholder.STRloungetv_tivo_ipaddress, dataholder.STRloungetv_tivo_mak)
# Create processes for TV Listing code and code to start bottle server
LSTlistings = Queue()
p1 = Process(target=tvlistings_process, args=(LSTlistings, ))
p2 = Process(target=start_bottle, args=())
# Start server
server_start()