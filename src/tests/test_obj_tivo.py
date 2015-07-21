from src.object_tivo import object_TIVO


def testTIVO(ipaddress, port, STRaccesskey="2531670703"):
    x = object_TIVO(ipaddress, port, STRaccesskey=STRaccesskey)
    result = False
    if ipaddress != x.getIP():
        result = True
        print ("TIVO Object Creation: Fail: - IP Address [E: " + ipaddress + "] [A: "+ x.getIP() + "]")
    if port != x.getPort():
        result = True
        print ("TIVO Object Creation: Fail - Port [E: " + port + "] [A: "+ x.getPort() + "]")
    if result != True:
        print ("TIVO Object Creation: Pass")

    result = x.sendCmd("IRCODE PAUSE\n\r")
    if not result:
        print ("Pause test: FAIL")
    else:
        print ("Pause test: PASS")

    result = x.sendCmd("IRCODE PLAY\n\r")
    if not result:
        print ("Play test: FAIL")
    else:
        print ("Play test: PASS")


print ("**** Test 1: TIVO ****")
testTIVO("192.168.0.112", 31339, STRaccesskey="2531670703")
print ("**********************")
