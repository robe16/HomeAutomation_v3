import src.tvlisting

#TODO rewrite for new method of dealing with listing data

def testListing1(channelID, id):
    result = src.tvlisting.get_xmllistings(channelID, id)
    if result==False:
        print("FAIL")
    else:
        print (result)

def testListing2():
    print (src.tvlisting.getall_xmllistings())


print ("*****************************************")
print ("****** Test: TV Listing Retrieval *******")
print ("*****************************************")
testListing1([108, "BBC", "92", "testimage.jpg", "tv"], "test")
print ("*****************************************")
print ("****** Test: Get details from enum ******")
print ("*****************************************")
testListing2()
print ("*****************************************")
print ("****************TEST  END****************")
print ("*****************************************")