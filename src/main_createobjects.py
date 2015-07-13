import dataholder
import object_tv_lg
import object_tivo


def create_objects():
    #LG TV
    if not dataholder.STRloungetv_lgtv_pairkey:
        dataholder.OBJloungetv = object_tv_lg.object_LGTV(dataholder.STRloungetv_lgtv_ipaddress, 8080, STRpairingkey=dataholder.STRloungetv_lgtv_pairkey)
    else:
        dataholder.OBJloungetv = object_tv_lg.object_LGTV(dataholder.STRloungetv_lgtv_ipaddress, 8080)
    #TIVO
    if not dataholder.STRloungetv_lgtv_pairkey:
        dataholder.OBJloungetivo = object_tivo.object_TIVO(dataholder.STRloungetv_tivo_ipaddress, 31339, STRaccesskey=dataholder.STRloungetv_tivo_mak)
    else:
        dataholder.OBJloungetivo = object_tivo.object_TIVO(dataholder.STRloungetv_tivo_ipaddress, 31339)