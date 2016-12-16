import datetime
import os
import time
import ast

from bottle import error, HTTPError
from bottle import get, post
from bottle import request, run, static_file, HTTPResponse, redirect, response

import cfg
from src.config.devices.config_devices import get_cfg_room_index, get_cfg_device_index, get_cfg_account_index
from src.config.users.config_users import check_user, update_user_channels
from src.tvlistings.tvlisting_getfromqueue import _check_tvlistingsqueue


################################################################################################

def start_bottle(q_dvcs, q_accs, queues):
    # '0.0.0.0' - all interfaces including the external one
    # 'localhost' - internal interfaces only
    global q_devices
    global q_accounts
    global q_dict
    q_devices = q_dvcs
    q_accounts = q_accs
    q_dict = queues
    run_bottle()

################################################################################################
# Provision of server config for clients
################################################################################################

from src.client_caches.setup import compile_setup
from src.client_caches.users import compile_users
from src.client_caches.weather import compile_weather
from src.client_caches.tvchannels import compile_tvchannels

@get('/cache/setup')
def cache_setup():
    try:
        return HTTPResponse(body=compile_setup(), status=200)
    except:
        return HTTPResponse(status=404)


@get('/cache/users')
def cache_users():
    try:
        return HTTPResponse(body=compile_users(), status=200)
    except:
        return HTTPResponse(status=404)


@get('/cache/weather')
def cache_weather():
    try:
        return HTTPResponse(body=compile_weather(), status=200)
    except:
        return HTTPResponse(status=404)


@get('/cache/tvchannels')
def cache_tvchannels():
    try:
        return HTTPResponse(body=compile_tvchannels(), status=200)
    except:
        return HTTPResponse(status=404)

from src.client_caches.tvlistings import compile_tvlistings

@get('/cache/tvlistings')
def cache_tvlistings():
    # try:
    #     return compile_tvlistings()
    # except:
    #     return HTTPError(404)
    return HTTPResponse(status=404)


################################################################################################
# User based operations
################################################################################################

from src.config.users.config_users import check_pin

@post('/user/pin')
def user_checkpin():
    check = check_pin(request.json['user'],
                      request.json['pin'])
    if check:
        return HTTPResponse(status=200)
    else:
        return HTTPResponse(status=401)


################################################################################################
# Handle requests for resource data
################################################################################################

@get('/data/device/<room_id>/<device_id>/<resource_requested>')
def get_data_device(room_id=False, device_id=False, resource_requested=False):
    #
    if (not room_id) or (not device_id) or (not resource_requested):
        raise HTTPError(404)
    #
    timestamp = datetime.datetime.now()
    #
    room_num = get_cfg_room_index(room_id)
    device_num = get_cfg_device_index(room_id, device_id)
    #
    if room_id == -1 or device_id == -1:
        raise HTTPError(404)
    #
    data_dict = {'data': resource_requested}
    #
    queue_item = {'timestamp': timestamp,
                  'response_queue': cfg.key_q_response_data,
                  'room_num': room_num,
                  'device_num': device_num,
                  'request': data_dict}
    #
    q_devices[room_num][device_num].put(queue_item)
    #
    time.sleep(0.1)
    #
    while datetime.datetime.now() < (timestamp + datetime.timedelta(seconds=cfg.request_timeout)):
        if not q_dict[cfg.key_q_response_data].empty():
            #
            rsp = q_dict[cfg.key_q_response_data].get()
            #
            if isinstance(rsp, bool):
                return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
            else:
                return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
            #
    raise HTTPError(500)


@get('/data/account/<account_id>/<resource_requested>')
def get_data_account(account_id=False, resource_requested=False):
    #
    if (not account_id) or (not resource_requested):
        raise HTTPError(404)
    #
    timestamp = datetime.datetime.now()
    #
    account_num = get_cfg_account_index(account_id)
    #
    if account_id == -1:
        raise HTTPError(404)
    #
    data_dict = {'data': resource_requested}
    #
    queue_item = {'timestamp': timestamp,
                  'response_queue': cfg.key_q_response_data,
                  'account_num': account_num,
                  'request': data_dict}
    #
    q_accounts[account_num].put(queue_item)
    #
    time.sleep(0.1)
    #
    while datetime.datetime.now() < (timestamp + datetime.timedelta(seconds=cfg.request_timeout)):
        if not q_dict[cfg.key_q_response_data].empty():
            #
            rsp = q_dict[cfg.key_q_response_data].get()
            #
            if isinstance(rsp, bool):
                return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
            else:
                return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
            #
    raise HTTPError(500)


################################################################################################
# Handle commands
################################################################################################

@post('/command/device/<room_id>/<device_id>')
def send_command_device(room_id=False, device_id=False):
    #
    if (not room_id) or (not device_id):
        raise HTTPError(404)
    #
    timestamp = datetime.datetime.now()
    #
    room_num = get_cfg_room_index(room_id)
    device_num = get_cfg_device_index(room_id, device_id)
    #
    if room_id == -1 or device_id == -1:
        raise HTTPError(404)
    #
    cmd_dict = request.json
    #
    queue_item = {'timestamp': timestamp,
                  'response_queue': cfg.key_q_response_command,
                  'room_num': room_num,
                  'device_num': device_num,
                  'request': cmd_dict}
    #
    q_devices[room_num][device_num].put(queue_item)
    #
    time.sleep(0.1)
    #
    while datetime.datetime.now() < (timestamp + datetime.timedelta(seconds=cfg.request_timeout)):
        if not q_dict[cfg.key_q_response_command].empty():
            #
            rsp = q_dict[cfg.key_q_response_command].get()
            #
            if isinstance(rsp, bool):
                return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
            else:
                return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
            #
    raise HTTPError(500)


@post('/command/account/<account_id>')
def send_command_account(account_id=False):
    #
    if not account_id:
        raise HTTPError(404)
    #
    timestamp = datetime.datetime.now()
    #
    account_num = get_cfg_account_index(account_id)
    #
    if account_id == -1:
        raise HTTPError(404)
    #
    cmd_dict = request.json()
    #
    queue_item = {'timestamp': timestamp,
                  'response_queue': cfg.key_q_response_command,
                  'account_num': account_num,
                  'request': cmd_dict}
    #
    q_accounts[account_num].put(queue_item)
    #
    time.sleep(0.1)
    #
    while datetime.datetime.now() < (timestamp + datetime.timedelta(seconds=cfg.request_timeout)):
        if not q_dict[cfg.key_q_response_command].empty():
            #
            rsp = q_dict[cfg.key_q_response_command].get()
            #
            if isinstance(rsp, bool):
                return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
            else:
                return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
            #
    raise HTTPError(500)


################################################################################################
# Update settings/server config
################################################################################################

# @post('/settings/<category>')
# def save_settings(category=''):
#     user = _check_user(request.get_cookie('user'))
#     if not user:
#         redirect('/web/login')
#     if get_userrole(user) != 'admin':
#         return HTTPResponse(body='You do not have user permissions to amend settings on the server.' +
#                                  'Please consult your administrator for further information.', status=400)
#     #
#     if category == 'tvguide':
#         data = request.body.read()
#         if data:
#             #TODO
#             # if update_channellist(data):
#                 return HTTPResponse(status=400)
#     elif category == 'devices':
#         data = request.body.read()
#         if data:
#             if write_config_devices(data):
#                 return HTTPResponse(status=200)
#         # TODO - put a timestamp in the config file so that users can check their command corresponds to latest configuration (query or json payload?)
#     else:
#         raise HTTPError(404)


################################################################################################
# Update user preferences
################################################################################################

@post('/preferences/<category>')
def save_preferences(category='-'):
    if category == 'tvguide':
        user = request.get_cookie('user')
        data = request.body
        if update_user_channels(user, data):
            return HTTPResponse(status=200)
    raise HTTPError(404)


################################################################################################
# Image files
################################################################################################

@get('/favicon.ico')
def send_favicon():
    root = os.path.join(os.path.dirname(__file__), '..', 'img/logo')
    return static_file('favicon.ico', root=root)


@get('/img/<category>/<filename>')
def get_image(category, filename):
    root = os.path.join(os.path.dirname(__file__), '..', 'img/{img_cat}'.format(img_cat=category))
    mimetype = filename.split('.')[1]
    return static_file(filename, root=root, mimetype='image/{mimetype}'.format(mimetype=mimetype))


################################################################################################
# This will allow for non-web UI to call for listings as XML payload.
# Put on hold for now as focus of current development scope on web-server access
################################################################################################
# @route('/tvlistings')
# def get_tvlistings():
#     listings = _check_tvlistingsqueue()
#     if not listings:
#         HTTPResponse(status=400)
#     channel = request.query.id or None
#     x = returnnonext_xml_all(listings, channel)
#     return HTTPResponse(body=x, status=200) if bool(x) else HTTPResponse(status=400)
################################################################################################


# def _check_user(user_cookie):
#     if not user_cookie:
#         return False
#     else:
#         if check_user(user_cookie):
#             return user_cookie
#         else:
#             return 'Guest'

def run_bottle():
    run(host='0.0.0.0', port=cfg.port_server, debug=True)
