import os
from bottle import route, get, post
from bottle import error, HTTPError
from bottle import request, run, static_file, HTTPResponse, redirect, response

from command_forwarder import cmd_fwrd
from config_devices import write_config_devices
from config_devices_create import create_device_object
from config_users import check_user, get_userrole, update_user_channels
from web_create_error import create_error
from web_create_pages import create_login, create_home, create_about, create_tvguide, create_device
from web_create_preferences import create_preference_tvguide
from web_create_settings import create_settings_devices, settings_devices_requests, create_settings_tvguide
from web_devices import refresh_tvguide


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
        return redirect('/web/home')


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
    tvlistings = _check_tvlistingsqueue()
    #
    if bool(request.query.group) and bool(request.query.device):
        return HTTPResponse(body=refresh_tvguide(tvlistings,
                                                 device = create_device_object(request.query.group, request.query.device),
                                                 group_name = request.query.group,
                                                 device_name = request.query.device,
                                                 user=user),
                            status=200) if bool(tvlistings) else HTTPResponse(status=400)
    else:
        return HTTPResponse(body=create_tvguide(user, tvlistings), status=200)


@get('/web/device/<group_name>/<device_name>')
def web_devices(group_name='', device_name=''):
    # Get and check user
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    #
    # Retrieve tvlistings from queue
    tvlistings = _check_tvlistingsqueue()
    # Create and return web interface page
    return HTTPResponse(body=create_device(user, tvlistings, group_name, device_name, request), status=200)


# @get('/web/settings/<page>')
# def web_settings(page=''):
#     user = _check_user(request.get_cookie('user'))
#     try:
#         if not user and page != 'login':
#             redirect('/web/login')
#         if get_userrole(user) != 'admin':
#             return HTTPResponse(body='You do not have user permissions to amend settings on the server.' +
#                                      'Please consult your administrator for further information.', status=400)
#         if page == 'devices':
#             return HTTPResponse(body=create_settings_devices(user), status=200)
#         elif page == 'tvguide':
#             return HTTPResponse(body=create_settings_tvguide(user), status=200)
#         else:
#             return HTTPResponse(body=create_error_404(user), status=400)
#     except:
#         return HTTPResponse(body=create_error_500(user), status=500)
#
#
# @route('/web/settings', method='GET')
# def web():
#     try:
#         body = settings_devices_requests(request)
#         if body:
#             return HTTPResponse(body=body, status=200)
#         else:
#             return HTTPResponse(status=400)
#     except:
#         return HTTPResponse(status=500)


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

@route('/command')
def send_command():
    #
    try:
        #
        rsp = cmd_fwrd(request)
        #
        if isinstance(rsp, bool):
            return HTTPResponse(status=200) if bool(rsp) else HTTPResponse(status=400)
        else:
            return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
    except:
        return HTTPResponse(status=400)


################################################################################################
# Update settings/server config
################################################################################################

# @post('/settings/<category>')
# def save_settings(category=''):
#     user = _check_user(request.get_cookie('user'))
#     try:
#         if not user:
#             redirect('/web/login')
#         if get_userrole(user) != 'admin':
#             return HTTPResponse(body='You do not have user permissions to amend settings on the server.' +
#                                      'Please consult your administrator for further information.', status=400)
#         if category == 'tvguide':
#             data = request.body.read()
#             if data:
#                 #TODO
#                 # if update_channellist(data):
#                     return HTTPResponse(status=400)
#         elif category == 'devices':
#             data = request.body.read()
#             if data:
#                 if write_config_devices(data):
#                     return HTTPResponse(status=200)
#             # TODO - put a timestamp in the config file so that users can check their command corresponds to latest configuration (query or json payload?)
#         return HTTPResponse(status=400)
#     except:
#         return HTTPResponse(status=500)


################################################################################################
# Update user preferences
################################################################################################

@post('/preferences/<category>')
def save_prefernces(category='-'):
    if _check_user(request.get_cookie('user')):
        if category == 'tvguide':
            user = request.get_cookie('user')
            data = request.body
            if update_user_channels(user, data):
                return HTTPResponse(status=200)
    else:
        return HTTPResponse(status=400)


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


def _check_tvlistingsqueue():
    return False


def _check_user(user_cookie):
    if not user_cookie:
        return False
    else:
        if check_user(user_cookie):
            return user_cookie
        else:
            return 'Guest'


def start_bottle(port):
    # '0.0.0.0' will listen on all interfaces including the external one (alternative for local testing is 'localhost')
    run(host='0.0.0.0', port=port, debug=True)