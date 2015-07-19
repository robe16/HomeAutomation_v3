from object_tv_lg import object_LGTV
from object_tivo import object_TIVO


def create_lgtv(STRloungetv_lgtv_ipaddress, STRpairingkey):
    if not STRpairingkey==None:
        return object_LGTV(STRloungetv_lgtv_ipaddress, 8080, STRpairingkey=STRpairingkey)
    else:
        return object_LGTV(STRloungetv_lgtv_ipaddress, 8080)


def create_tivo(STRloungetv_tivo_ipaddress, STRaccesskey):
    if not STRaccesskey==None:
        return object_TIVO(STRloungetv_tivo_ipaddress, 31339, STRaccesskey=STRaccesskey)
    else:
        return object_TIVO(STRloungetv_tivo_ipaddress, 31339)