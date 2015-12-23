from ebaysdk.trading import Connection as Trading
import json, re

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


# ref:
# http://stackoverflow.com/questions/250271/python-regex-how-to-get-positions-of-matches
# http://www.tutorialspoint.com/python/python_dictionary.htm
# http://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#the-name-argument
# http://www.pythonforbeginners.com/python-on-the-web/web-scraping-with-beautifulsoup/
# https://pymotw.com/2/json/
# http://developer.ebay.com/devzone/xml/docs/reference/ebay/getmyebayselling.html
# http://stackoverflow.com/questions/4990718/python-about-catching-any-exception
# http://www.tutorialspoint.com/python/python_files_io.htm
