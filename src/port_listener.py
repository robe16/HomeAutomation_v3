import os

from bottle import HTTPError
from bottle import get, post
from bottle import request, run, static_file, HTTPResponse

from config.bindings.config_bindings import get_cfg_group_seq, get_cfg_thing_seq, get_cfg_info_seq
from lists.resources.english import *
from log.log import log_error, log_general

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
# Create log message
################################################################################################

def log_msg(request, resource):
    #
    ip = request['REMOTE_ADDR']
    msg = '{ip} - {resource}'.format(ip=ip, resource=resource)
    #
    return msg

################################################################################################
# Provision of server config for clients
################################################################################################

from client_caches.setup import compile_setup
from client_caches.users import compile_users
from client_caches.tvchannels import compile_tvchannels

@get(uri_cache_setup)
def cache_setup():
    log = log_msg(request, uri_cache_setup)
    try:
        log_general(log)
        return HTTPResponse(body=compile_setup(), status=200)
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        return HTTPResponse(status=404)


@get(uri_cache_users)
def cache_users():
    log = log_msg(request, uri_cache_setup)
    try:
        log_general(log)
        return HTTPResponse(body=compile_users(), status=200)
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        return HTTPResponse(status=404)


@get(uri_cache_tvchannels)
def cache_tvchannels():
    log = log_msg(request, uri_cache_setup)
    try:
        log_general(log)
        return HTTPResponse(body=compile_tvchannels(), status=200)
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        return HTTPResponse(status=404)


# TODO: details of cache update subscription caught here - now to set so any update to respective jsons will inform client
@post(uri_cache_subscribe)
def cache_subscribe():
    log = log_msg(request, uri_cache_setup)
    try:
        #
        r = request
        #
        categories = request.json['categories']
        ipaddress = request.json['ipaddress']
        port = request.json['port']
        #
        log_general(log)
        return HTTPResponse(status=200)
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        return HTTPResponse(status=404)


################################################################################################
# User based operations
################################################################################################

from config.users.config_users import check_pin

@post(uri_user_pin)
def user_checkpin():
    log = log_msg(request, uri_cache_setup)
    check = check_pin(request.json['user'],
                      request.json['pin'])
    if check:
        log_general('{log} - {user} - {passfail}'.format(log=log, user=request.json['user'], passfail='pass'))
        return HTTPResponse(status=200)
    else:
        log_general('{log} - {user} - {passfail}'.format(log=log, user=request.json['user'], passfail='fail'))
        return HTTPResponse(status=401)


################################################################################################
# Handle requests for resource data
################################################################################################

@get(uri_data_infoservice)
def get_data_infoservice(service=False, resource_requested=False):
    #
    global infoservices
    #
    log = log_msg(request, uri_cache_setup)
    #
    try:
        #
        if (not service) or (not resource_requested):
            log_error('{log} - {error}'.format(log=log, error='URI invalid'))
            raise HTTPError(404)
        #
        try:
            info_seq = get_cfg_info_seq(service)
        except Exception as e:
            log_error('{log} - {error}'.format(log=log, error=e))
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
        log_general(log)
        return response
        #
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        raise HTTPError(500)


@get(uri_data_device)
def get_data_device(group=False, thing=False, resource_requested=False):
    #
    global devices
    #
    log = log_msg(request, uri_cache_setup)
    #
    try:
        #
        if (not group) or (not thing) or (not resource_requested):
            log_error('{log} - {error}'.format(log=log, error='URI invalid'))
            raise HTTPError(404)
        #
        try:
            group_seq = get_cfg_group_seq(group)
            thing_seq = get_cfg_thing_seq(group, thing)
        except Exception as e:
            log_error('{log} - {error}'.format(log=log, error=e))
            raise HTTPError(404)
        #
        data_dict = {'data': resource_requested}
        #
        rsp = devices[group_seq][thing_seq].getData(data_dict)
        #
        log_general(log)
        #
        if isinstance(rsp, bool):
            return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
        else:
            return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
        #
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        raise HTTPError(500)


################################################################################################
# Handle commands
################################################################################################

@post(uri_command_device)
def send_command_device(group=False, thing=False):
    #
    global devices
    #
    log = log_msg(request, uri_cache_setup)
    #
    try:
        #
        if (not group) or (not thing):
            log_error('{log} - {error}'.format(log=log, error='URI invalid'))
            raise HTTPError(404)
        #
        try:
            group_seq = get_cfg_group_seq(group)
            thing_seq = get_cfg_thing_seq(group, thing)
        except Exception as e:
            log_error('{log} - {error}'.format(log=log, error=e))
            raise HTTPError(404)
        #
        cmd_dict = request.json
        #
        rsp = devices[group_seq][thing_seq].sendCmd(cmd_dict)
        #
        log_general(log)
        #
        if isinstance(rsp, bool):
            return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
        else:
            return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
        #
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
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
    log = log_msg(request, uri_cache_setup)
    try:
        root = os.path.join(os.path.dirname(__file__), 'imgs/logo')
        log_general(log)
        return static_file('favicon.ico', root=root)
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        raise HTTPError(500)


@get(uri_image)
def get_image(category, filename):
    log = log_msg(request, uri_cache_setup)
    try:
        root = os.path.join(os.path.dirname(__file__), 'imgs/{img_cat}'.format(img_cat=category))
        mimetype = filename.split('.')[1]
        log_general(log)
        return static_file(filename, root=root, mimetype='image/{mimetype}'.format(mimetype=mimetype))
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        raise HTTPError(500)

################################################################################################

def run_bottle(self_port):
    host='0.0.0.0'
    log_general('Bottle started: listening on {host}:{port}'.format(host=host, port=self_port))
    run(host=host, port=self_port, debug=True)
