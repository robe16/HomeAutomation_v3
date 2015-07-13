import ConfigParser
import object_tv_lg
import object_tivo

#Lounge TV
STRloungetv_lgtv_ipaddress = None
STRloungetv_lgtv_pairkey = None
STRloungetv_tivo_ipaddress = None
STRloungetv_tivo_mak = None
#Audio
STRrocki_ipaddress = None
#Heating
STRnesturl_api = "https://developer-api.nest.com"
STRnest_pincode = None
STRnest_token = None
STRnest_tokenexp = None
#Nest thermostat - unique client details for application
STRnest_clientID = "170016da-432a-4ca0-aa37-426a2117d7a2"
STRnest_clientSecret = "6NqNFOfF1BAHByR8T6dn0OLTI"


def create_objects():
    #LG TV
    if not STRloungetv_lgtv_pairkey:
        OBJloungetv = object_tv_lg.object_LGTV(STRloungetv_lgtv_ipaddress, 8080, STRpairingkey=STRloungetv_lgtv_pairkey)
    else:
        OBJloungetv = object_tv_lg.object_LGTV(STRloungetv_lgtv_ipaddress, 8080)
    #TIVO
    if not STRloungetv_lgtv_pairkey:
        OBJloungetivo = object_tivo.object_TIVO(STRloungetv_tivo_ipaddress, 31339, STRaccesskey = STRloungetv_tivo_mak)
    else:
        OBJloungetivo = object_tivo.object_TIVO(STRloungetv_tivo_ipaddress, 31339)


def read_config():
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    #
    STRloungetv_lgtv_ipaddress = Config.options("Lounge")['LGTV_ipaddress']
    STRloungetv_lgtv_pairkey = Config.options("Lounge")['LGTV_pairkey']
    STRloungetv_tivo_ipaddress = Config.options("Lounge")['TIVO_ipaddress']
    STRloungetv_tivo_mak = Config.options("Lounge")['TIVO_mak']
    STRrocki_ipaddress = Config.options("Kitchen")['Rocki_ipaddress']