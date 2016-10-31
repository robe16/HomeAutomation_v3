import os
import datetime
import time
from bottle import route, get, post
from bottle import error, HTTPError
from bottle import request, run, static_file, HTTPResponse, redirect, response

import cfg

from config_devices import write_config_devices
from config_devices import get_cfg_structure_name, get_cfg_room_name, get_cfg_device_name, get_cfg_account_name
from config_devices import get_cfg_structure_index, get_cfg_room_index, get_cfg_device_index, get_cfg_account_index
from config_users import check_user, get_userrole, update_user_channels
from web_create_error import create_error
from web_create_pages import create_login, create_home, create_about, create_tvguide, create_device
from web_create_preferences import create_preference_tvguide
from web_create_settings import create_settings_devices, settings_devices_requests, create_settings_tvguide
# from web_devices import refresh_tvguide

from tvlisting_getfromqueue import _check_tvlistingsqueue


################################################################################################

def start_bottle(port, q_dvcs, q_accs, queues):
    # '0.0.0.0' - all interfaces including the external one
    # 'localhost' - internal interfaces only
    global q_devices
    global q_accounts
    global q_dict
    q_devices = q_dvcs
    q_accounts = q_accs
    q_dict = queues
    run_bottle(port)

################################################################################################
# Provision of server config for clients
################################################################################################

#TODO

@get('/cfg/structure')
def cfg_structure():
    # open config file
    # run through list and extract rooms and devices
    # present in json format
    # return to client
    return True

'''
{
    "structure": {
        "1": {
            "room_id": "1",
            "room_name": "Lounge",
            "room_name_alt": ["lounge", "living room", "front room"]
            "devices": {
                "0": {
                    "device_id": "0",
                    "device_type": "tivo",
                    "device_name": "tivo",
                    "device_name_alt": ["tivo", "virgin", "virgin media", "set top", "cable"]
                },
                "1": {
                    "device_id": "1",
                    "device_type": "tv_lg_netcast",
                    "device_name": "tv",
                    "device_name_alt": ["tv", "television"]
                }
            }
        },
        "2": {
            "room_id": "2",
            "room_name": "Kitchen",
            "room_name_alt": ["kitchen"]
            "devices": {}
        }
     }
 }
'''

################################################################################################
# Web UI
################################################################################################

@get('/')
def web_redirect():
    redirect('/web/')


@get('/web/login')
def web_login():
    user = request.query.user
    if not user:
        return HTTPResponse(body=create_login(), status=200)
    else:
        response.set_cookie('user', user, path='/', secret=None)
        return redirect('/web/')


@get('/web/logout')
def web_logout():
    response.delete_cookie('user')
    return redirect('/web/login')


@get('/web/')
@get('/web/home/')
def web_home():
    # Get and check user
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    #
    return HTTPResponse(body=create_home(user), status=200)


@get('/web/about/')
def web_about():
    # Get and check user
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    #
    return HTTPResponse(body=create_about(user), status=200)


@get('/web/tvguide')
def web_tvguide():
    # Get and check user
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    #
    # Retrieve tvlistings from queue
    tvlistings = _check_tvlistingsqueue(q_dict[cfg.key_q_tvlistings])
    #
    # if bool(request.query.group) and bool(request.query.device):
    #     return HTTPResponse(body=refresh_tvguide(tvlistings,
    #                                              device = False, #create_device_object(request.query.group, request.query.device),
    #                                              group_name = request.query.group,
    #                                              device_name = request.query.device,
    #                                              user=user),
    #                         status=200) if bool(tvlistings) else HTTPResponse(status=400)
    # else:
    return HTTPResponse(body=create_tvguide(user, tvlistings), status=200)


@get('/web/device/<structure_id>/<room_id>/<device_id>')
def web_devices(structure_id=False, room_id=False, device_id=False):
    #
    if (not structure_id) or (not room_id) or (not device_id):
        raise HTTPError(404)
    #
    # Get and check user
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    #
    structure_num = get_cfg_structure_index(structure_id)
    room_num = get_cfg_room_index(structure_id, room_id)
    device_num = get_cfg_device_index(structure_id, room_id, device_id)
    #
    if structure_id == -1 or room_id == -1 or device_id == -1:
        raise HTTPError(404)
    #
    timestamp = datetime.datetime.now()
    queue_item = {'timestamp': timestamp,
                  'response_queue': cfg.key_q_response_web_device,
                  'structure_num': structure_num,
                  'room_num': room_num,
                  'device_num': device_num,
                  'user': request.get_cookie('user')}
    #
    q_devices[structure_num][room_num][device_num].put(queue_item)
    #
    time.sleep(0.1)
    #
    while datetime.datetime.now() < (timestamp + datetime.timedelta(seconds=cfg.request_timeout)):
        if not q_dict[cfg.key_q_response_web_device].empty():
            return create_device(user,
                                 q_dict[cfg.key_q_response_web_device].get(),
                                 '{structure_name}: {room_name}: {device_name}'.format(structure_name=get_cfg_structure_name(structure_id),
                                                                                       room_name=get_cfg_room_name(structure_id, room_id),
                                                                                       device_name=get_cfg_device_name(structure_id, room_id, device_id)),
                                 '{structure_name}: {room_name}: {device_name}'.format(structure_name=get_cfg_structure_name(structure_id),
                                                                                       room_name=get_cfg_room_name(structure_id, room_id),
                                                                                       device_name=get_cfg_device_name(structure_id, room_id, device_id)))
    #
    raise HTTPError(500)


@get('/web/account/<structure_id>/<account_id>')
def web_accounts(structure_id=False, account_id=False):
    #
    if (not structure_id) or (not account_id):
        raise HTTPError(404)
    #
    # Get and check user
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    #
    structure_num = get_cfg_structure_index(structure_id)
    account_num = get_cfg_account_index(structure_id, account_id)
    #
    if structure_id == -1 or account_id == -1:
        raise HTTPError(404)
    #
    timestamp = datetime.datetime.now()
    queue_item = {'timestamp': timestamp,
                  'response_queue': cfg.key_q_response_web_device,
                  'structure_num': structure_num,
                  'account_num': account_num,
                  'user': request.get_cookie('user')}
    #
    q_accounts[structure_num][account_num].put(queue_item)
    #
    time.sleep(0.1)
    #
    while datetime.datetime.now() < (timestamp + datetime.timedelta(seconds=cfg.request_timeout)):
        if not q_dict[cfg.key_q_response_web_device].empty():
            return create_device(user,
                                 q_dict[cfg.key_q_response_web_device].get(),
                                 '{structure_name}: {account_name}'.format(structure_name=get_cfg_structure_name(structure_id),
                                                                           account_name=get_cfg_account_name(structure_id, account_id)),
                                 '{structure_name}: {account_name}'.format(structure_name=get_cfg_structure_name(structure_id),
                                                                           account_name=get_cfg_account_name(structure_id, account_id)))
    #
    raise HTTPError(500)


# @get('/web/settings/<page>')
# def web_settings(page=''):
#     user = _check_user(request.get_cookie('user'))
#     if not user:
#         redirect('/web/login')
#     if get_userrole(user) != 'admin':
#         return HTTPResponse(body='You do not have user permissions to amend settings on the server.' +
#                                  'Please consult your administrator for further information.', status=400)
#     if page == 'devices':
#         return HTTPResponse(body=create_settings_devices(user), status=200)
#     elif page == 'tvguide':
#         return HTTPResponse(body=create_settings_tvguide(user), status=200)
#     else:
#         raise HTTPError(404)


# @get('/web/settings')
# def web():
#     return HTTPResponse(body=settings_devices_requests(request), status=200)


@get('/web/preferences/<page>')
def web_preferences(page=''):
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    if page == 'tvguide':
        return HTTPResponse(body=create_preference_tvguide(user), status=200)
    else:
        raise HTTPError(404)


@get('/web/static/<folder>/<filename>')
def get_resource(folder, filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__), ('web/static/{folder}'.format(folder=folder))))


################################################################################################
# Handle commands
################################################################################################


@get('/command/device/<structure_id>/<room_id>/<device_id>')
@post('/command/device/<structure_id>/<room_id>/<device_id>')
def send_command_device(structure_id=False, room_id=False, device_id=False):
    #
    if (not structure_id) or (not room_id) or (not device_id):
        raise HTTPError(404)
    #
    timestamp = datetime.datetime.now()
    #
    structure_num = get_cfg_structure_index(structure_id)
    room_num = get_cfg_room_index(structure_id, room_id)
    device_num = get_cfg_device_index(structure_id, room_id, device_id)
    #
    if structure_id == -1 or room_id == -1 or device_id == -1:
        raise HTTPError(404)
    #
    cmd_dict = dict(request.query)
    #
    queue_item = {'timestamp': timestamp,
                  'response_queue': cfg.key_q_response_command,
                  'structure_num': structure_num,
                  'room_num': room_num,
                  'device_num': device_num,
                  'request': cmd_dict}
    #
    q_devices[structure_num][room_num][device_num].put(queue_item)
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


@get('/command/account/<structure_id>/<account_id>')
@post('/command/account/<structure_id>/<account_id>')
def send_command_account(structure_id=False, account_id=False):
    #
    if (not structure_id) or (not account_id):
        raise HTTPError(404)
    #
    timestamp = datetime.datetime.now()
    #
    structure_num = get_cfg_structure_index(structure_id)
    account_num = get_cfg_account_index(structure_id, account_id)
    #
    if structure_id == -1 or account_id == -1:
        raise HTTPError(404)
    #
    cmd_dict = dict(request.query)
    #
    queue_item = {'timestamp': timestamp,
                  'response_queue': cfg.key_q_response_command,
                  'structure_num': structure_num,
                  'account_num': account_num,
                  'request': cmd_dict}
    #
    q_devices[structure_num][account_num].put(queue_item)
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
    if _check_user(request.get_cookie('user')):
        if category == 'tvguide':
            user = request.get_cookie('user')
            data = request.body
            if update_user_channels(user, data):
                return HTTPResponse(status=200)
    else:
        raise HTTPError(404)


################################################################################################
# Image files
################################################################################################

@get('/favicon.ico')
def send_favicon():
    root = os.path.join(os.path.dirname(__file__), '..', 'img/logo')
    return static_file('favicon.ico', root=root)


@get('/img/<category>/<filename:re:.*\.png>')
def get_image(category, filename):
    root = os.path.join(os.path.dirname(__file__), '..', 'img/{img_cat}'.format(img_cat=category))
    return static_file(filename, root=root, mimetype='image/png')


################################################################################################
# Error pages/responses
################################################################################################

@error(404)
def error404(error):
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    return HTTPResponse(body=create_error(user, 404), status=404)


@error(500)
def error500(error):
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    return HTTPResponse(body=create_error(user, 500), status=500)


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


def _check_user(user_cookie):
    if not user_cookie:
        return False
    else:
        if check_user(user_cookie):
            return user_cookie
        else:
            return 'Guest'

def run_bottle(port):
    run(host='0.0.0.0', port=port, debug=True)
