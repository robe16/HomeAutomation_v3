from src.object_tivo import object_TIVO


def testTIVO(ipaddress, port):
    x = object_TIVO(ipaddress, port)
    result = False
    if ipaddress != x.getIP():
        result = True
        print ("Fail: IP Address [E: " + ipaddress + "] [A: "+ x.getIP() + "]")
    if port != x.getPort():
        result = True
        print ("Fail: Port [E: " + port + "] [A: "+ x.getPort() + "]")
    if result != True:
        print ("Pass")


print ("**** Test 1: TIVO ****")
testTIVO("192.168.0.110", "123")
