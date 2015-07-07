from src.object_tv_lg import object_LGTV


def testLGTV(ipaddress, port, key=None):
    if key!=None:
        x = object_LGTV(ipaddress, port, STRpairingkey=key)
    else:
        x = object_LGTV(ipaddress, port)
    result = False

    if ipaddress != x.getIP():
        result = True
        print ("Object IP Address: FAIL [E: " + ipaddress + "] [A: "+ x.getIP() + "]")
    else:
        print ("Object IP Address: PASS")

    if port != x.getPort():
        result = True
        print ("Object Port: FAIL [E: " + port + "] [A: "+ x.getPort() + "]")
    else:
        print ("Object Port: PASS")

    if key != x.getPairingkey():
        result = True
        print ("Object Pairing Key: FAIL [E: " + key + "] [A: "+ x.getPairingkey() + "]")
    else:
        print ("Object Pairing Key: PASS")

##    if result != True:
##        print ("Object: Pass")

    result = x.showPairingkey()
    if result==True:
        print ("Show Key Test: PASS")
    else:
        print ("Show Key Test: FAIL - "+result)
        
    print ("**Enter pairing key value:")
    inptX = input()
    x.setPairingkey(inptX)
    if inptX==x.getPairingkey():
        print ("User Entered Pairing Key Test: PASS")
    else:
        print ("User Entered Pairing Key Test: FAIL - [input: "+inptX+" stored: "+x.getPairingkey()+"]")

    result = x._pairDevice()
    if result==True:
        print ("Pair Device Test: PASS")
    else:
        print ("Pair Device Test: FAIL - "+result)


print ("**** Test 1: LGTV with no pairing key****")
objX = testLGTV("192.168.0.111", "8080")

##print ("**** Test 2: LGTV with pairing key****")
##objX = testLGTV("192.168.0.111", "8080", key="123")
##
##print ("**** Test 3: Intentional LGTV error - port number ****")
##objX = testLGTV("192.168.0.111", "12345")
