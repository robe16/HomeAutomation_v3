import dataholder
from config import read_config
import create_objects
from src.bottle import route, run, static_file
from object_tv_lg import object_LGTV
from object_tivo import object_TIVO


def __init__():
    read_config()

    #Create objects
    object_LGTV = create_objects.create_lgtv(dataholder.STRloungetv_lgtv_ipaddress,dataholder.STRloungetv_lgtv_pairkey)
    object_TIVO = create_objects.create_lgtv(dataholder.STRloungetv_tivo_ipaddress, dataholder.STRloungetv_tivo_mak)


@route('/device/<room>/<device>/<command>')
def send_command(room="-", device="-", command="-"):
    #TODO
    if room=="lounge":
        if device=="lgtv":
            return object_LGTV.sendCmd(command)
        elif device=="tivo":
            return object_TIVO.sendCmd(command)
        else:
            return "Error"
    else:
        return "Error"

@route('/image/<category>/<filename:re:.*\.png>')
def send_image(category, filename):
    return static_file(filename, root='./img/%s' % category, mimetype='image/png')


run(host='localhost', port=8080, debug=True)