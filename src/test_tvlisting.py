import tvlisting


def testListing1(channelID):
    result = tvlisting.getlistings(channelID)
    if result==False:
        print("FAIL")
    else:
        count = 0
        while count < len(result):
            print (result[count])
            count+=1

def testListing2():
    print (tvlisting.getalllistings())


print ("*****************************************")
print ("****** Test: TV Listing Retrieval *******")
print ("*****************************************")
testListing1("92")
print ("*****************************************")
print ("****** Test: Get details from enum ******")
print ("*****************************************")
testListing2()
print ("*****************************************")
print ("****************TEST  END****************")
print ("*****************************************")