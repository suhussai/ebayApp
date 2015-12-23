from ebaysdk.trading import Connection as Trading
from bs4 import BeautifulSoup
import json

ids = ['','','','']
for fileName, index in [('appid',0), ('devid',1), ('certid',2), ('tokenid',3)]:
    fileHandler = open("IGNORE_" + fileName, "r")
    ids[index] = fileHandler.read().rstrip()
    fileHandler.close()

try:    
    api = Trading(appid=ids[0], devid=ids[1], certid=ids[2], token=ids[3])
    # response = api.execute('GetMyeBaySelling', {'SoldList': {'DurationInDays' : '1'}})
    # #print(json.dumps(response.dict(), indent=2))
    # for transaction in response.dict()['SoldList']['OrderTransactionArray']['OrderTransaction']:
    #     name = transaction['Transaction']['Item']['Title']
    #     try:
    #         item_price = transaction['Transaction']['TotalPrice']['value']
    #     except:
    #         item_price = "Not Found"

    #     print(name + ", " + item_price)

        
    

    #response.dict()['SoldList']['OrderTransactionArray']['OrderTransaction'][0]['Transaction']['Item']['Title']


    # response = api.execute('GetOrders',{'NumberOfDays':'1'})
    # print(json.dumps(response.dict(), indent=2))
    # print(response.dict())
    # print(response.reply)


except Exception as e:
    print(e)

