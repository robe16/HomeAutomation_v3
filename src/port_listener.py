import os

from bottle import HTTPError
from bottle import get, post
from bottle import request, run, static_file, HTTPResponse

from config.bindings.config_bindings import get_cfg_group_seq, get_cfg_thing_seq, get_cfg_info_seq
from lists.resources.english import *
from log.log import log_error

################################################################################################

devices = {}
infoservices = {}

################################################################################################

def start_bottle(_devices, _infoservices, self_port):
    #
    global devices
    devices = _devices
    global infoservices
    infoservices= _infoservices
    #
    run_bottle(self_port)

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

@get(uri_cache_setup)
def cache_setup():
    try:
        return HTTPResponse(body=compile_setup(), status=200)
    except Exception as e:
        log_error('{error}'.format(error=e))
        return HTTPResponse(status=404)


@get(uri_cache_users)
def cache_users():
    try:
        return HTTPResponse(body=compile_users(), status=200)
    except Exception as e:
        log_error('{error}'.format(error=e))
        return HTTPResponse(status=404)


@get(uri_cache_tvchannels)
def cache_tvchannels():
    try:
        return HTTPResponse(body=compile_tvchannels(), status=200)
    except Exception as e:
        log_error('{error}'.format(error=e))
        return HTTPResponse(status=404)


# TODO: details of cache update subscription caught here - now to set so any update to respective jsons will inform client
@post(uri_cache_subscribe)
def cache_subscribe():
    try:
        #
        r = request
        #
        categories = request.json['categories']
        ipaddress = request.json['ipaddress']
        port = request.json['port']
        #
        return HTTPResponse(status=200)
    except Exception as e:
        log_error('{error}'.format(error=e))
        return HTTPResponse(status=404)


################################################################################################
# User based operations
################################################################################################

from config.users.config_users import check_pin

@post(uri_user_pin)
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

@get(uri_data_infoservice)
def get_data_infoservice(service=False, resource_requested=False):
    #
    global infoservices
    #
    try:
        #
        if (not service) or (not resource_requested):
            raise HTTPError(404)
        #
        try:
            info_seq = get_cfg_info_seq(service)
        except Exception as e:
            raise HTTPError(404)
        #
        data_dict = {'data': resource_requested}
        #
        if len(request.query.decode()) > 0:
            data_dict.update(request.query.decode())
        #
        #
        rsp = infoservices[info_seq].getData(data_dict)
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
        log_error('{error}'.format(error=e))
        raise HTTPError(500)


@get(uri_data_device)
def get_data_device(group=False, thing=False, resource_requested=False):
    #
    global devices
    #
    try:
        #
        if (not group) or (not thing) or (not resource_requested):
            raise HTTPError(404)
        #
        try:
            group_seq = get_cfg_group_seq(group)
            thing_seq = get_cfg_thing_seq(group, thing)
        except Exception as e:
            raise HTTPError(404)
        #
        data_dict = {'data': resource_requested}
        #
        rsp = devices[group_seq][thing_seq].getData(data_dict)
        #
        if isinstance(rsp, bool):
            return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
        else:
            return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
        #
    except Exception as e:
        log_error('{error}'.format(error=e))
        raise HTTPError(500)


################################################################################################
# Handle commands
################################################################################################

@post(uri_command_device)
def send_command_device(group=False, thing=False):
    #
    global devices
    #
    try:
        #
        if (not group) or (not thing):
            raise HTTPError(404)
        #
        try:
            group_seq = get_cfg_group_seq(group)
            thing_seq = get_cfg_thing_seq(group, thing)
        except Exception as e:
            raise HTTPError(404)
        #
        cmd_dict = request.json
        #
        rsp = devices[group_seq][thing_seq].sendCmd(cmd_dict)
        #
        if isinstance(rsp, bool):
            return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
        else:
            return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
        #
    except Exception as e:
        log_error('{error}'.format(error=e))
        raise HTTPError(500)


################################################################################################
# Update user preferences
################################################################################################

# TODO - to allow submission of user's preferences for things like TV channel favourites

# @post('/preferences/<category>')
# def save_preferences(category='-'):
#     if category == 'tvguide':
#         user = request.get_cookie('user')
#         data = request.body
#         if update_user_channels(user, data):
#             return HTTPResponse(status=200)
#     raise HTTPError(404)


################################################################################################
# Image files
################################################################################################

@get(uri_favicon)
def send_favicon():
    root = os.path.join(os.path.dirname(__file__), 'imgs/logo')
    return static_file('favicon.ico', root=root)


@get(uri_image)
def get_image(category, filename):
    root = os.path.join(os.path.dirname(__file__), 'imgs/{img_cat}'.format(img_cat=category))
    mimetype = filename.split('.')[1]
    return static_file(filename, root=root, mimetype='image/{mimetype}'.format(mimetype=mimetype))

################################################################################################

def run_bottle(self_port):
    run(host='0.0.0.0', port=self_port, debug=True)
