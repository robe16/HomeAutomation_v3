import dataholder
from config import read_config
import create_objects
from object_tv_lg import object_LGTV
from object_tivo import object_TIVO
import os, time, threading
from tvlisting import getall_listings, getall_xmllistings, get_xmllistings
from bottle import route, request, run, static_file, HTTPResponse
from multiprocessing import Process, Queue
from io import BytesIO


def start_bottle():
    run(host='localhost', port=8080, debug=True)

def server_start():
    tvlistings_startprocess()
    p2.start()

def server_end():
    p1.terminate()
    p2.terminate()

def tvlistings_startprocess():
    p1.start()

def tvlistings_process(q):
    # 604800 secs = 7 days
    while True:
        tvlistings(q)
        time.sleep(604800)

def tvlistings(q):
    q.put(getall_listings())

@route('/index')
def index():
    x = "Message"
    return HTTPResponse(body=x, status=200)


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
    elif room=="lounge" and device=="lgtv":
        return HTTPResponse(status=200) if dataholder.OBJloungetv.sendCmd(command) else HTTPResponse(status=400)
    elif room=="lounge" and device=="tivo":
        return HTTPResponse(status=200) if dataholder.OBJloungetivo.sendCmd(command) else HTTPResponse(status=400)
    return HTTPResponse(status=400)

@route('/tvlistings')
def get_tvlistings():
    channel = request.query.id or False
    x = get_xmllistings(q.get()[0]) if bool(channel) else getall_xmllistings(q.get()[0])
    return HTTPResponse(body=x, status=200) if bool(x) else HTTPResponse(status=400)

@route('/img/<category>/<filename:re:.*\.png>')
def get_image(category, filename):
    root = os.path.join(os.path.dirname(__file__), '..', 'img/%s' % category)
    return static_file(filename, root=root, mimetype='image/png')


# Get configuration
read_config()
# Create objects
dataholder.OBJloungetv = create_objects.create_lgtv(dataholder.STRloungetv_lgtv_ipaddress,dataholder.STRloungetv_lgtv_pairkey)
dataholder.OBJloungetivo = create_objects.create_tivo(dataholder.STRloungetv_tivo_ipaddress, dataholder.STRloungetv_tivo_mak)
# GCreate processes for TV Listing code and code to start bottle server
q = Queue()
p1 = Process(target=tvlistings_process, args=(q,))
p2 = Process(target=start_bottle, args=())
# Start server
server_start()