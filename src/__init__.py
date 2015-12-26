from multiprocessing import Process, Queue
import os
import time
import string
import random

import nest_static_vars
from config_devices import write_config_devices, read_json_devices, read_config_devices
from config_nest import write_config_nest, read_json_nest, read_config_nest
from config_users import check_user, get_usertheme
from object_tv_lg import object_LGTV
from object_tivo import object_TIVO
from web_pages import create_login, create_home, create_device_group, create_tvguide, create_about
from web_settings import create_settings_devices, create_settings_tvguide, create_settings_nest
from web_tvlistings import get_tvlistings_for_device
from tvlisting import build_channel_array, returnnonext_xml_all
from bottle import route, request, run, static_file, HTTPResponse, template, redirect, response


def start_bottle():
    # '0.0.0.0' will listen on all interfaces including the external one (alternative for local testing is 'localhost')
    run(host='0.0.0.0', port=1622, debug=True)


def server_start():
    tvlistings_startprocess()
    p2.start()


def server_end():
    p1.terminate()
    p2.terminate()


def tvlistings_startprocess():
    p1.start()


def tvlistings_process():
    time.sleep(5)
    # 604800 secs = 7 days
    while True:
        #list_listings.put(getall_listings())
        list_listings.put(build_channel_array())
        time.sleep(604800)


@route('/')
@route('/web/')
def web_redirect():
    redirect('/web/home')


@route('/web/login')
@route('/web/login.php')
def web():
    user = request.query.user
    if not user:
        return HTTPResponse(body=create_login(), status=200)
    else:
        response.set_cookie('user', user, path='/', secret=None)
        return redirect('/web/home')


@route('/web/logout')
def web():
    response.delete_cookie('user')
    return redirect('/web/login')


@route('/web/<page>')
def web(page=""):
    user = _check_user(request.get_cookie('user'))
    if not user and page != 'login':
        redirect('/web/login')
    theme = get_usertheme(user)
    listings = _check_tvlistingsqueue()
    if page == 'home':
        return HTTPResponse(body=create_home(user, theme, ARRobjects), status=200)
    elif page == 'tvguide':
        return HTTPResponse(body=create_tvguide(user, theme, listings, ARRobjects), status=200)
    elif page == 'settings_devices':
        return HTTPResponse(body=create_settings_devices(user, theme, ARRobjects), status=200)
    elif page == 'settings_tvguide':
        return HTTPResponse(body=create_settings_tvguide(user, theme, listings, ARRobjects), status=200)
    elif page == 'settings_nest':
        return HTTPResponse(body=create_settings_nest(user,
                                                      theme,
                                                      ARRobjects,
                                                      nest_static_vars.STRnest_clientID,
                                                      ARRnestData[0],
                                                      randomstring),
                            status=200)
    elif page == 'about':
        return HTTPResponse(body=create_about(user, theme, ARRobjects), status=200)
    else:
        return HTTPResponse(body='An error has occurred', status=400)


@route('/web/<room>/<group>')
def web(room="", group=""):
    user = _check_user(request.get_cookie('user'))
    if not user:
        return HTTPResponse(body=create_login(), status=200)
    theme = get_usertheme(user)
    listings = _check_tvlistingsqueue()
    # If query for tv listings availability, return html code
    available = bool(request.query.tvguide) or False
    if available:
        return HTTPResponse(body=get_tvlistings_for_device(listings,
                                                           ARRobjects,
                                                           room,
                                                           group,
                                                           user=user),
                            status=200) if bool(listings) else HTTPResponse(status=400)
    # Create and return web interface page
    try:
        return HTTPResponse(body=create_device_group(user, theme, listings, ARRobjects, room, group), status=200)
    except:
        return HTTPResponse(body='An error has occurred', status=400)


@route('/web/static/<folder>/<filename>')
def get_image(folder, filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__), ('web/static/{}'.format(folder))))


@route('/device/<room>/<group>/<device>/<command>')
def send_command(room="-", group="-", device="-", command="-"):
    #
    x = 0
    while x < len(ARRobjects):
        if ARRobjects[x][0] == room:
            y = 0
            while y < len(ARRobjects[x][1]):
                if ARRobjects[x][1][y][0] == group:
                    list_devices = ARRobjects[x][1][y][1]
                    z = 0
                    while z < len(list_devices):
                        if list_devices[z].getName().replace(" ", "").lower() == device:
                            command = request.query.id if command == 'channel' else command
                            response = list_devices[z].sendCmd(command)
                            return HTTPResponse(body=str(response),
                                                status=200) if bool(response) else HTTPResponse(status=400)
                        z += 1
                y += 1
        x += 1
    #
    return HTTPResponse(status=400)
    # if room=="lounge" and device=="lgtv" and command=="appslist":
    #     APPtype = request.query.type or 3
    #     APPindex = request.query.index or 0
    #     APPnumber = request.query.number or 0
    #     x = OBJloungetv.getApplist(APPtype=APPtype, APPindex=APPindex, APPnumber=APPnumber)
    #     return HTTPResponse(body=x, status=200) if bool(x) else HTTPResponse(status=400)
    # elif room=="lounge" and device=="lgtv" and command=="appicon":
    #     auid = request.query.auid or False
    #     name = request.query.name or False
    #     if not bool(auid) or not bool(name):
    #         return HTTPResponse(status=400)
    #     x = OBJloungetv.getAppicon(auid, name)
    #     return HTTPResponse(body=x, status=200, content_type='image/png') if bool(x) else HTTPResponse(status=400)
    # # TV Command
    # if room=="lounge" and device=="lgtv":
    #     return HTTPResponse(status=200) if OBJloungetv.sendCmd(command) else HTTPResponse(status=400)
    # # TiVo Command
    # elif room=="lounge" and device=="tivo":
    #     if command=="channel":
    #         channo = request.query.id or False
    #         if channo:
    #             return HTTPResponse(status=200) if OBJloungetivo.sendCmd(channo) else HTTPResponse(status=400)
    #         else:
    #             HTTPResponse(status=400)
    #     else:
    #         return HTTPResponse(status=200) if OBJloungetivo.sendCmd(command) else HTTPResponse(status=400)
    # else:
    #     return HTTPResponse(status=400)


@route('/tvlistings')
def get_tvlistings():
    listings = _check_tvlistingsqueue()
    if not listings:
        HTTPResponse(status=400)
    channel = request.query.id or None
    x = returnnonext_xml_all(listings, channel)
    return HTTPResponse(body=x, status=200) if bool(x) else HTTPResponse(status=400)


@route('/settings/<x>', method='GET')
@route('/settings/<x>', method='POST')
def save_settings(x="-"):
    if x == 'nest':
        pincode = request.query.pincode
        if not bool(pincode):
            return HTTPResponse(status=400)
        if write_config_nest([pincode, ARRnestData[1], ARRnestData[2]]):
            ARRnestData[0] = pincode
            return HTTPResponse(status=200)
        else:
            return HTTPResponse(status=400)
    elif x == 'devices':
        data = request.body
        if data:
            tempARR = read_json_devices(data.getvalue())
            if write_config_devices(tempARR):
                ARRobjects = tempARR
                return HTTPResponse(status=200)
            else:
                return HTTPResponse(status=400)
        else:
            return HTTPResponse(status=400)
    else:
        return HTTPResponse(status=400)


@route('/favicon.ico')
def send_favicon():
    root = os.path.join(os.path.dirname(__file__), '..', 'img/logo/favicon.ico')
    return static_file('favicon.ico', root=root)


@route('/img/<category>/<filename:re:.*\.png>')
def get_image(category, filename):
    root = os.path.join(os.path.dirname(__file__), '..', 'img/{}'.format(category))
    return static_file(filename, root=root, mimetype='image/png')


def _check_tvlistingsqueue():
    # Check listings in queue
    if not list_listings.empty():
        temp = list_listings.get()
        list_listings.put(temp)
        return temp
    else:
        return False


def _check_user(user_cookie):
    if not user_cookie:
        return False
    else:
        if check_user(user_cookie):
            return user_cookie
        else:
            return 'Guest'


#TODO temp variable here with property postcode (replace with settings page input etc.)
postcode='ls27'
# Create objects from configuration file
randomstring = (postcode.join('-').join(random.choice(string.ascii_lowercase) for i in range(5)))
ARRobjects = read_config_devices()
ARRnestData = read_config_nest()
#
# Create processes for TV Listing code and code to start bottle server
list_listings = Queue()
p1 = Process(target=tvlistings_process)
p2 = Process(target=start_bottle)
# Start server
server_start()
