from object_tv_lg import object_LGTV
from object_tivo import object_TIVO


def create_lgtv(STRname, STRloungetv_lgtv_ipaddress, STRpairingkey, BOOLtvguide_use, STRgroup):
    if not STRpairingkey==None:
        return object_LGTV(STRname, STRloungetv_lgtv_ipaddress, 8080, STRpairingkey=STRpairingkey, BOOLtvguide_use=BOOLtvguide_use, STRgroup=STRgroup)
    else:
        return object_LGTV(STRname, STRloungetv_lgtv_ipaddress, 8080, BOOLtvguide_use=BOOLtvguide_use, STRgroup=STRgroup)


def create_tivo(STRname, STRloungetv_tivo_ipaddress, STRaccesskey, BOOLtvguide_use, STRgroup):
    if not STRaccesskey==None:
        return object_TIVO(STRname, STRloungetv_tivo_ipaddress, 31339, STRaccesskey=STRaccesskey, BOOLtvguide_use=BOOLtvguide_use, STRgroup=STRgroup)
    else:
        return object_TIVO(STRname, STRloungetv_tivo_ipaddress, 31339, BOOLtvguide_use=BOOLtvguide_use, STRgroup=STRgroup)