from multiprocessing import Process, Queue
import os
import time
import string
import random

import nest_static_vars
from config_devices import write_config_devices, create_device_object_array
from config_users import check_user, get_userrole, update_user_channels
from web_create_pages import create_login, create_home, create_about, create_tvguide, create_device
from web_devices import refresh_tvguide
from web_create_settings import create_settings_devices, create_settings_tvguide, create_settings_nest
from web_create_preferences import create_preference_tvguide
from web_tvlistings import html_listings_user_and_all, _listings_html
from web_create_error import create_error_404, create_error_500
from __web_testpage import create_test
from tvlisting import build_channel_array, returnnonext_xml_all
from bottle import route, request, run, static_file, HTTPResponse, template, redirect, response

def start_bottle():
    # '0.0.0.0' will listen on all interfaces including the external one (alternative for local testing is 'localhost')
    run(host='0.0.0.0', port=1600, debug=True)


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


# TEST PAGE here for checking and testing design ideas
@route('/testpage')
def web():
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    return HTTPResponse(body=create_test(user, arr_devices), status=200)


@route('/web/<page>')
def web(page=""):
    user = _check_user(request.get_cookie('user'))
    try:
        if not user and page != 'login':
            redirect('/web/login')
        tvlistings = _check_tvlistingsqueue()
        if page == 'home':
            return HTTPResponse(body=create_home(user, arr_devices), status=200)
        elif page == 'tvguide':
            tvguide_request = bool(request.query.tvguide) or False
            if tvguide_request:
                return HTTPResponse(body=refresh_tvguide(tvlistings,
                                                         user=user),
                                    status=200) if bool(tvlistings) else HTTPResponse(status=400)
            return HTTPResponse(body=create_tvguide(user, arr_devices, tvlistings), status=200)
        elif page == 'about':
            return HTTPResponse(body=create_about(user, arr_devices), status=200)
        else:
            return HTTPResponse(body=create_error_404(user, arr_devices), status=400)
    except:
        return HTTPResponse(body=create_error_500(user, arr_devices), status=500)


@route('/web/device/<group_name>/<device_name>')
def web(group_name='', device_name=''):
    user = _check_user(request.get_cookie('user'))
    # try:
    if not user:
        redirect('/web/login')
    dvc = _get_device(group_name, device_name)
    tvlistings = _check_tvlistingsqueue()
    # If query for tv listings availability, return html code
    tvguide_request = bool(request.query.tvguide) or False
    if tvguide_request:
        device_url = 'device/{group}/{device}'.format(group=group_name, device=device_name)
        return HTTPResponse(body=refresh_tvguide(tvlistings,
                                                 device=dvc,
                                                 device_url=device_url,
                                                 user=user),
                            status=200) if bool(tvlistings) else HTTPResponse(status=400)
    # Create and return web interface page
    return HTTPResponse(body=create_device(user, tvlistings, arr_devices, group_name, device_name), status=200)
    # except:
    #     return HTTPResponse(body=create_error_500(user, arr_devices), status=500)


@route('/web/settings/<page>')
def web(page=""):
    user = _check_user(request.get_cookie('user'))
    try:
        if not user and page != 'login':
            redirect('/web/login')
        if get_userrole(user) != 'admin':
            return HTTPResponse(body='You do not have user permissions to amend settings on the server.' +
                                     'Please consult your administrator for further information.', status=400)
        if page == 'devices':
            return HTTPResponse(body=create_settings_devices(user, arr_devices), status=200)
        elif page == 'tvguide':
            return HTTPResponse(body=create_settings_tvguide(user, arr_devices), status=200)
        else:
            return HTTPResponse(body=create_error_404(user, arr_devices), status=400)
    except:
        return HTTPResponse(body=create_error_500(user, arr_devices), status=500)


@route('/web/preferences/<page>')
def web(page=""):
    user = _check_user(request.get_cookie('user'))
    try:
        if not user and page != 'login':
            redirect('/web/login')
        if page == 'tvguide':
            return HTTPResponse(body=create_preference_tvguide(user, arr_devices), status=200)
        else:
            return HTTPResponse(body=create_error_404(user, arr_devices), status=400)
    except:
        return HTTPResponse(body=create_error_500(user, arr_devices), status=500)


@route('/web/static/<folder>/<filename>')
def get_image(folder, filename):
    try:
        return static_file(filename, root=os.path.join(os.path.dirname(__file__), ('web/static/{}'.format(folder))))
    except:
        return HTTPResponse(status=400)


@route('/device/<group_name>/<device_name>/<command>')
def send_command(group_name="-", device_name="-", command="-"):
    #
    dvc = _get_device(group_name, device_name)
    #
    try:
        response = dvc.sendCmd(command, request)
        if isinstance(response, bool) or isinstance(response, int):
            return HTTPResponse(body=str(response), status=200) if bool(response) else HTTPResponse(status=400)
        else:
            return response
            #static_file(filename, root=os.path.join(os.path.dirname(__file__), ('web/static/{}'.format(folder))))
    except:
        return HTTPResponse(status=400)


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
    #TODO!!!!
    # if x == 'nest':
    #     pincode = request.query.pincode
    #     if not bool(pincode):
    #         return HTTPResponse(status=400)
    #     if write_config_nest([pincode, ARRnestData[1], ARRnestData[2]]):
    #         ARRnestData[0] = pincode
    #         return HTTPResponse(status=200)
    #     else:
    #         return HTTPResponse(status=400)
    #TODO - for receipt of new device json
    # elif x == 'devices':
    #     data = request.body
    #     if data:
    #         tempARR = read_json_devices(data.getvalue())
    #         if write_config_devices(tempARR):
    #             ARRobjects = tempARR
    #             return HTTPResponse(status=200)
    #         else:
    #             return HTTPResponse(status=400)
    #     else:
    #         return HTTPResponse(status=400)
    # else:
    return HTTPResponse(status=400)


@route('/preferences/<x>', method='POST')
def save_prefernces(x='-'):
    if _check_user(request.get_cookie('user')):
        if x == 'tvguide':
            user = request.get_cookie('user')
            data = request.body
            if update_user_channels(user, data):
                return HTTPResponse(status=200)
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


def _get_device(group_name, device_name):
    #
    for device_group in arr_devices:
        # Get group name - as some groups do not have a name, default this to '-'
        if not device_group['name'] == '':
            grp_name = device_group['name']
        else:
            grp_name = '-'
        #
        if grp_name.lower().replace(' ','') == group_name:
            #
            for objdevice in device_group['devices']:
                if objdevice.getName().lower().replace(' ','') == device_name:
                    return objdevice
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
arr_devices = create_device_object_array()
#
# Create processes for TV Listing code and code to start bottle server
list_listings = Queue()
p1 = Process(target=tvlistings_process)
p2 = Process(target=start_bottle)
# Start server
server_start()
