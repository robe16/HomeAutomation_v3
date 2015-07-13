from src.object_tv_lg import object_LGTV


def testLGTV(ipaddress, port, key=None):
    if key!=None:
        x = object_LGTV(ipaddress, port, STRpairingkey=key)
    else:
        x = object_LGTV(ipaddress, port)

    if ipaddress != x.getIP():
        print ("*Object IP Address: FAIL [E: " + ipaddress + "] [A: "+ x.getIP() + "]")
    else:
        print ("*Object IP Address: PASS")

    if port != x.getPort():
        print ("*Object Port: FAIL [E: " + port + "] [A: "+ x.getPort() + "]")
    else:
        print ("*Object Port: PASS")

    if key != x.getPairingkey():
        print ("*Object Pairing Key: FAIL [E: " + key + "] [A: "+ x.getPairingkey() + "]")
    else:
        print ("*Object Pairing Key: PASS")

    if key==None:
        result = x.showPairingkey()
        if not result:
            print ("*Show Key Test: FAIL")
            return
        else:
            print ("*Show Key Test: PASS")

        print ("**Enter pairing key value:")
        inptX = input()
        x.setPairingkey(inptX)
        if inptX==x.getPairingkey():
            print ("*User Entered Pairing Key Test: PASS")
        else:
            print ("*User Entered Pairing Key Test: FAIL - [input: "+inptX+" stored: "+x.getPairingkey()+"]")

        result = x._pairDevice()
        if not result:
            print ("*Pair Device Test: FAIL")
            return
        else:
            print ("*Pair Device Test: PASS")

    result = x.sendCmd("25")
    if not result:
        print ("*Volume Up test: FAIL")
        return
    else:
        print ("*Volume Up test: PASS")


print ("*****************************************")
print ("**** Test 1: LGTV with no pairing key****")
print ("*****************************************")
ipaddress = "192.168.0.111"
port = "8080"
pairkey="397905"
print (ipaddress+":"+port)
objX = testLGTV(ipaddress, port, key=pairkey)
print ("*****************************************")
print ("****************TEST  END****************")
print ("*****************************************")

##print ("**** Test 2: LGTV with pairing key****")
##objX = testLGTV("192.168.0.111", "8080", key="123")
##
##print ("**** Test 3: Intentional LGTV error - port number ****")
##objX = testLGTV("192.168.0.111", "12345")
