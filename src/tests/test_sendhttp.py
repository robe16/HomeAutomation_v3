from src.send_cmds import sendHTTP


def testHTTP(ipaddress, connection, expected, data=""):
    x = sendHTTP(ipaddress, connection, data=data)
    print (ipaddress)

    if expected and x!=False:
        print ("Test Result: PASS")
    elif expected==x:
        print ("Test Result: PASS")
    else:
        print ("Test Result: FAIL")


print ("**** Test 1: Google & /search ****")
testHTTP("https://www.google.co.uk/search", "close", True)

print ("**** Test 2: Internal IP with port number ****")
testHTTP("http://192.168.0.100:32400/web/index.html", "close", True)

print ("**** Test 3: Redirect ****")
testHTTP("http://steamcommunity.com/id/robe_16/home/", "close", True)

print ("**** Test 4: Intentional HTTP Fail ****")
testHTTP("https://www.google.co.uk/asdfg", "close", False)

print ("**** Test 5: 'http://' correction ****")
testHTTP("www.google.co.uk/search", "close", True)
