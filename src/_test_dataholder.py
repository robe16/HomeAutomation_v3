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
print ("Rocki IP address: "+str(dataholder.STRrocki_ipaddress))
print ("Nest Pincode: "+str(dataholder.STRnest_pincode))
print ("Nest Token: "+str(dataholder.STRnest_token))
print ("Nest Token expiry: "+str(dataholder.STRnest_tokenexp))
print ("*****************************************")
print ("****************TEST  END****************")
print ("*****************************************")