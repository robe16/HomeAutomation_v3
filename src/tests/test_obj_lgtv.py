from src.object_tv_lg import object_LGTV
import time


def testLGTV(ipaddress, port, key=None):
    x = object_LGTV(ipaddress, port, STRpairingkey=key) if key!=None else object_LGTV(ipaddress, port)

    print "*Object IP Address: %s" % ("PASS" if ipaddress==x.getIP() else ("FAIL [E: %s] [A: %s]" % (ipaddress, x.getIP())))
    print "*Object Port: %s" % ("PASS" if port==x.getPort() else ("FAIL [E: %s] [A: %s]" % (port, x.getPort())))
    print "*Object Pairing Key: %s" % ("PASS" if key==x.getPairingkey() else ("FAIL [E: %s] [A: %s]" % (key, x.getPairingkey())))
    print "Paired? %s" % ("Yes" if x._BOOLpaired else "No")

    if key==None:
        print "*Show Key Test: %s" % ("PASS" if x.showPairingkey() else "FAIL")

        print "**Enter pairing key value:"
        inptX = input()
        x.setPairingkey(inptX)
        print "*User Entered Pairing Key Test: %s" % ("PASS" if inptX==x.getPairingkey() else ("FAIL - [input: %s] [stored: %s]" % (inptX, x.getPairingkey())))

        print "*Pair Device Test: PASS" if x._pairDevice() else "*Pair Device Test: FAIL"

    print "*Volume Up test: %s" % ("PASS" if x.sendCmd("volup") else "FAIL")
    time.sleep(2)
    print "*Home test: %s" % ("PASS" if x.sendCmd("home") else "FAIL")
    time.sleep(2)
    print "*OK test: %s" % ("PASS" if x.sendCmd("ok") else "FAIL")

    result = x.getApplist()
    if not result:
        print "*App List test: FAIL"
    else:
        print "*App List test: PASS"
        print "                %s" % result


print ("*****************************************")
print ("**** Test 1: LGTV with no pairing key****")
print ("*****************************************")
ipaddress = "192.168.0.111"
port = "8080"
pairkey="397905"
print "%s:%s" % (ipaddress, port)
objX = testLGTV(ipaddress, port, key=pairkey)
print ("*****************************************")
print ("****************TEST  END****************")
print ("*****************************************")

##print ("**** Test 2: LGTV with pairing key****")
##objX = testLGTV("192.168.0.111", "8080", key="123")
##
##print ("**** Test 3: Intentional LGTV error - port number ****")
##objX = testLGTV("192.168.0.111", "12345")
