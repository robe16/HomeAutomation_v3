import dataholder
from config import write_config_json, read_config_json
from object_tv_lg import object_LGTV
from object_tivo import object_TIVO
from web_createpages import create_home, create_device_group, create_tvguide, create_settings_rooms, create_settings_devices, create_settings_nest, create_about
import os, time
from tvlisting import getall_listings, getall_xmllistings, get_xmllistings
from bottle import route, request, run, static_file, HTTPResponse, template, redirect
from multiprocessing import Process, Queue
import string
import random

def start_bottle():
    run(host='0.0.0.0', port=1614, debug=True) # '0.0.0.0' will listen on all interfaces including the external one (alternative for local testing is 'localhost')

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

@route('/test/config/write')
def get_config_write():
    return HTTPResponse(body=write_config_json(ARRobjects), status=200)

@route('/test/config/read')
def get_config_read():
    return HTTPResponse(body=read_config_json(), status=200)

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
        return HTTPResponse(body=create_home(ARRobjects), status=200)
    elif page=="tvguide":
        return HTTPResponse(body=create_tvguide(listings, ARRobjects), status=200)
    elif page=="settings_rooms":
        return HTTPResponse(body=create_settings_rooms(ARRobjects), status=200)
    elif page=="settings_devices":
        return HTTPResponse(body=create_settings_devices(ARRobjects), status=200)
    elif page=="settings_nest":
        return HTTPResponse(body=create_settings_nest(ARRobjects, dataholder.STRnest_clientID, dataholder.STRnest_pincode, randomstring), status=200)
    elif page=="about":
        return HTTPResponse(body=create_about(ARRobjects), status=200)
    else:
        return HTTPResponse(body="An error has occurred", status=400)

@route('/web/<room>/<group>')
def web(room="", group=""):
    if not LSTlistings.empty():
        temp = LSTlistings.get()
        LSTlistings.put(temp)
        listings=temp[0]
    else:
        listings = False
    print create_device_group(listings, ARRobjects, room, group)
    return HTTPResponse(body=create_device_group(listings, ARRobjects, room, group), status=200)
    try:
        return HTTPResponse(body=create_device_group(listings, ARRobjects, room, group), status=200)
    except:
        return HTTPResponse(body="An error has occurred", status=400)

@route('/web/static/<folder>/<filename>')
def get_image(folder, filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__), ('web/static/%s' % folder)))

@route('/device/<room>/<group>/<device>/<command>')
def send_command(room="-", group="-", device="-", command="-"):
    #
    x=0
    while x<len(ARRobjects):
        if ARRobjects[x][0]==room:
            y=0
            while y<len(ARRobjects[x][1]):
                if ARRobjects[x][1][y][0]==group:
                    LSTdevices=ARRobjects[x][1][y][1]
                    z=0
                    while z<len(LSTdevices):
                        if LSTdevices[z].getName().replace(" ", "").lower()==device:
                            command = request.query.id if command=="channel" else command
                            return HTTPResponse(status=200) if bool(LSTdevices[z].sendCmd(command)) else HTTPResponse(status=400)
                        z+=1
                y+=1
        x+=1
    #
    return HTTPResponse(status=400)
    '''if room=="lounge" and device=="lgtv" and command=="appslist":
        APPtype = request.query.type or 3
        APPindex = request.query.index or 0
        APPnumber = request.query.number or 0
        x = OBJloungetv.getApplist(APPtype=APPtype, APPindex=APPindex, APPnumber=APPnumber)
        return HTTPResponse(body=x, status=200) if bool(x) else HTTPResponse(status=400)
    elif room=="lounge" and device=="lgtv" and command=="appicon":
        auid = request.query.auid or False
        name = request.query.name or False
        if not bool(auid) or not bool(name):
            return HTTPResponse(status=400)
        x = OBJloungetv.getAppicon(auid, name)
        return HTTPResponse(body=x, status=200, content_type='image/png') if bool(x) else HTTPResponse(status=400)
    # TV Command
    if room=="lounge" and device=="lgtv":
        return HTTPResponse(status=200) if OBJloungetv.sendCmd(command) else HTTPResponse(status=400)
    # TiVo Command
    elif room=="lounge" and device=="tivo":
        if command=="channel":
            channo = request.query.id or False
            if channo:
                return HTTPResponse(status=200) if OBJloungetivo.sendCmd(channo) else HTTPResponse(status=400)
            else:
                HTTPResponse(status=400)
        else:
            return HTTPResponse(status=200) if OBJloungetivo.sendCmd(command) else HTTPResponse(status=400)
    else:
        return HTTPResponse(status=400)'''

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
        write_config_json(ARRobjects)
        return HTTPResponse(status=200)
    else:
        return HTTPResponse(status=400)

@route('/favicon.ico')
def send_favicon():
    root = os.path.join(os.path.dirname(__file__), '..', 'img/logo/favicon.ico')
    return static_file('favicon.ico', root=root)

@route('/img/<category>/<filename:re:.*\.png>')
def get_image(category, filename):
    root = os.path.join(os.path.dirname(__file__), '..', 'img/%s' % category)
    return static_file(filename, root=root, mimetype='image/png')

# Get configuration
#read_config()
# Create objects from configuration file
randomstring = (''.join(random.choice(string.ascii_lowercase) for i in range(5)))
ARRobjects = read_config_json()
#
# Create processes for TV Listing code and code to start bottle server
LSTlistings = Queue()
p1 = Process(target=tvlistings_process, args=(LSTlistings, ))
p2 = Process(target=start_bottle, args=())
# Start server
server_start()

# Code template for iterating through object array
def foobar(ARRobjects):
    x=0
    while x<len(ARRobjects):
        room=ARRobjects[x][0]
        y=0
        while y<len(ARRobjects[x][1]):
            group=ARRobjects[x][1][y][0]
            z=0
            while z<len(ARRobjects[x][1][y][1]):
                deviceobject=ARRobjects[x][1][y][1][z]
                z+=1
            y+=1
        x+=1