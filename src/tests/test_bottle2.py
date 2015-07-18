from src.bottle import route, run

@route('/structure/')
def structure_json():
    return "Details of the structure\n"

@route('/room/<name>')
def get_devices(name="-"):
    return "List of devices in %s\n" % (name)

@route('/device/<name>/<device>/<command>')
def send_command(name="-", device="-", command="-"):
    return "Command will be sent to specific device\nRoom: %s\nDevice: %s\nCommand: %s\n" % (name, device, command)

@route('/device/<name>/<device>/<command>')
def get_infocommand(name="-", device="-", command="-"):
    return "Command will be sent to specific device\nRoom: %s\nDevice: %s\nCommand: %s\n" % (name, device, command)

# @route('/recipes/<name>', method='DELETE' )
# def recipe_delete( name="Mystery Recipe" ):
#     return "DELETE RECIPE " + name
#
# @route('/recipes/<name>', method='PUT')
# def recipe_save( name="Mystery Recipe" ):
#     return "SAVE RECIPE " + name

run(host='localhost', port=8080, debug=True)

# curl -X GET http://localhost:8080/structure/
# curl -X GET http://localhost:8080/room/lounge
# curl -X GET http://localhost:8080/device/lounge/lgtv/volup
# curl -X GET http://localhost:8080/device/lounge/lgtv/channels