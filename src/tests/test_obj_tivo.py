from src.object_tivo import object_TIVO


def testTIVO(ipaddress, port, STRaccesskey="2531670703"):
    x = object_TIVO(ipaddress, port, STRaccesskey=STRaccesskey)

    print "*Object IP Address: %s" % ("PASS" if ipaddress==x.getIP() else ("FAIL [E: %s] [A: %s]" % (ipaddress, x.getIP())))
    print "*Object Port: %s" % ("PASS" if port==x.getPort() else ("FAIL [E: %s] [A: %s]" % (port, x.getPort())))

    print "Pause test: %s" % ("PASS" if x.sendCmd("pause") else "FAIL")
    print "Play test: %s" % ("PASS" if x.sendCmd("play") else "FAIL")


print ("**** Test 1: TIVO ****")
testTIVO("192.168.0.112", 31339, STRaccesskey="2531670703")
print ("**********************")
