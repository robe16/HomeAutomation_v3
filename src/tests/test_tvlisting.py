import src.tvlisting


def testListing1(channelID, id):
    result = src.tvlisting.getlistings(channelID, id)
    if result==False:
        print("FAIL")
    else:
        print (result)

def testListing2():
    print (src.tvlisting.getalllistings())


print ("*****************************************")
print ("****** Test: TV Listing Retrieval *******")
print ("*****************************************")
testListing1([108, "BBC", "92"], "test")
print ("*****************************************")
print ("****** Test: Get details from enum ******")
print ("*****************************************")
testListing2()
print ("*****************************************")
print ("****************TEST  END****************")
print ("*****************************************")