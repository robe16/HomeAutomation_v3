import dataholder
from config import read_config


print ("*****************************************")
print ("********** Test: dataholder.py **********")
print ("*****************************************")
read_config()
print ("TV IP address: "+str(dataholder.STRloungetv_lgtv_ipaddress))
print ("TV Pair key: "+str(dataholder.STRloungetv_lgtv_pairkey))
print ("TIVO IP address: "+str(dataholder.STRloungetv_tivo_ipaddress))
print ("TIVO Mak: "+str(dataholder.STRloungetv_tivo_mak))
print ("*****************************************")
print ("****************TEST  END****************")
print ("*****************************************")