import os
from bottle import Bottle, get, post, hook
from bottle import error, HTTPError
from bottle import request, run, static_file, HTTPResponse, redirect, response
import cfg
from log.console_messages import print_error
from config.users.config_users import check_user, update_user_channels


################################################################################################

devices = {}
accounts = {}
infoservices = {}

################################################################################################

def start_bottle(_devices, _accounts, _infoservices):
    #
    global devices
    global accounts
    global infoservices
    devices = _devices
    accounts = _accounts
    infoservices = _infoservices
    #
    run_bottle()

################################################################################################
# Enable cross domain scripting
################################################################################################

def enable_cors(response):
    #
    # Wildcard '*' for Access-Control-Allow-Origin as mirrorUI will be hosted in 'file://' on device
    #
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    # response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    #
    return response

################################################################################################
# Provision of server config for clients
################################################################################################

from client_caches.setup import compile_setup
from client_caches.users import compile_users
from client_caches.tvchannels import compile_tvchannels

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


@get('/cache/tvchannels')
def cache_tvchannels():
    try:
        return HTTPResponse(body=compile_tvchannels(), status=200)
    except:
        return HTTPResponse(status=404)

from client_caches.tvlistings import compile_tvlistings

# @get('/cache/tvlistings')
# def cache_tvlistings():
#     # try:
#     #     return compile_tvlistings()
#     # except:
#     #     return HTTPError(500)
#     return HTTPResponse(status=404)


################################################################################################
# User based operations
################################################################################################

from config.users.config_users import check_pin

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

@get('/data/info/<service>/<resource_requested>')
def get_data_infoservice(service=False, resource_requested=False):
    #
    global infoservices
    #
    try:
        #
        if (not service) or (not resource_requested):
            raise HTTPError(404)
        #
        data_dict = {'data': resource_requested}
        #
        rsp = infoservices[service].getData(data_dict)
        #
        response = HTTPResponse()
        enable_cors(response)
        #
        if isinstance(rsp, bool):
            if rsp:
                response.status = 200
            else:
                response.status=400
        else:
            if bool(rsp):
                response.body=str(rsp)
                response.status=200
            else:
                response.status=400
        #
        return response
        #
    except Exception as e:
        print_error('{error}'.format(error=e))
        raise HTTPError(500)


@get('/data/device/<room_id>/<device_id>/<resource_requested>')
def get_data_device(room_id=False, device_id=False, resource_requested=False):
    #
    global devices
    #
    try:
        #
        if (not room_id) or (not device_id) or (not resource_requested):
            raise HTTPError(404)
        #
        data_dict = {'data': resource_requested}
        #
        rsp = devices[room_id][device_id].getData(data_dict)
        #
        if isinstance(rsp, bool):
            return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
        else:
            return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
        #
    except Exception as e:
        print_error('{error}'.format(error=e))
        raise HTTPError(500)


@get('/data/account/<account_id>/<resource_requested>')
def get_data_account(account_id=False, resource_requested=False):
    #
    global accounts
    #
    try:
        #
        if (not account_id) or (not resource_requested):
            raise HTTPError(404)
        #
        data_dict = {'data': resource_requested}
        #
        rsp = accounts[account_id].getData(data_dict)
        #
        if isinstance(rsp, bool):
            if rsp:
                response.status = 200
            else:
                response.status=400
        else:
            if bool(rsp):
                response.body=str(rsp)
                response.status=200
            else:
                response.status=400
        #
        return response
        #
    except Exception as e:
        print_error('{error}'.format(error=e))
        raise HTTPError(500)


################################################################################################
# Handle commands
################################################################################################

@post('/command/device/<room_id>/<device_id>')
def send_command_device(room_id=False, device_id=False):
    #
    global devices
    #
    try:
        #
        if (not room_id) or (not device_id):
            raise HTTPError(404)
        #
        cmd_dict = request.json
        #
        rsp = devices[room_id][device_id].sendCmd(cmd_dict)
        #
        if isinstance(rsp, bool):
            return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
        else:
            return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
        #
    except Exception as e:
        print_error('{error}'.format(error=e))
        raise HTTPError(500)


@post('/command/account/<account_id>')
def send_command_account(account_id=False):
    #
    global accounts
    #
    try:
        #
        if not account_id:
            raise HTTPError(404)
        #
        cmd_dict = request.json()
        #
        rsp = accounts[account_id].sendCmd(cmd_dict)
        #
        if isinstance(rsp, bool):
            return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
        else:
            return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
        #
    except Exception as e:
        print_error('{error}'.format(error=e))
        raise HTTPError(500)


################################################################################################
# Update user preferences
################################################################################################

# TODO

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

def run_bottle():
    run(host='0.0.0.0', port=cfg.port_server, debug=True)
