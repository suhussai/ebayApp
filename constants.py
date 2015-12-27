days = "1"
targetHtmlFile = "target.html" 
ids = ['','','','']
for fileName, index in [('appid',0), ('devid',1), ('certid',2), ('tokenid',3)]:
    fileHandler = open("IGNORE_" + fileName, "r")
    ids[index] = fileHandler.read().rstrip()
    fileHandler.close()

try:
    shippingInfo = pickle.load(open("itemInfo.p", "rb"))
except:
    shippingInfo = {}

