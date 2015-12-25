from ebaysdk.trading import Connection as Trading
from getShippingLabelInfo import shippingInfo
import json, re

ids = ['','','','']
for fileName, index in [('appid',0), ('devid',1), ('certid',2), ('tokenid',3)]:
    fileHandler = open("IGNORE_" + fileName, "r")
    ids[index] = fileHandler.read().rstrip()
    fileHandler.close()

itemsSold = {}
days = '10'
try:    
    api = Trading(appid=ids[0], devid=ids[1], certid=ids[2], token=ids[3])
    response = api.execute('GetMyeBaySelling', 
                           {'SoldList': 
                            {'DurationInDays' : days} 
                        }
    )
    orderIDList = []
    for transaction in response.dict()['SoldList']['OrderTransactionArray']['OrderTransaction']:
        orderId = transaction['Transaction']['OrderLineItemID']
        orderIDList.append(orderId)
        itemsSold[orderId] = {} # create element

    response = api.execute('GetOrders',
                           {'OrderIDArray': {'OrderID': orderIDList},
                            'NumberOfDays': days}
    )

    for order in response.dict()['OrderArray']['Order']:
        orderID = order['OrderID'] 
        if orderID in itemsSold.keys():
            # it is a sold item
            # add to itemsSold dict
            for transaction in order['TransactionArray']['Transaction']: 
                item_name = transaction['Item']['Title']
                try:
                    item_tracking_number = transaction['ShippingDetails']['ShipmentTrackingDetails']['ShipmentTrackingNumber']
                except Exception as e:
                    item_tracking_number = "N\A"
                    
            order_date = order['CreatedTime'] # ex: 2015-12-16T21:13:54.000Z
            item_total_price = order['Total']['value']
            itemsSold[orderID]['ItemName'] = item_name
            itemsSold[orderID]['ItemPrice'] = item_total_price
            itemsSold[orderID]['ItemTrackingNumber'] = item_tracking_number
            itemsSold[orderID]['ItemDate'] = order_date #[:order_date.find("T")]

    orderIDs = itemsSold.keys()
    for orderID in orderIDs:
        info = shippingInfo.get(itemsSold[orderID]['ItemTrackingNumber'], None)
        if info is not None:
            itemsSold[orderID]['ShippingStatus'] = info['ShippingStatus']
            itemsSold[orderID]['BuyerName'] = info['BuyerName']
            itemsSold[orderID]['ShippingLabelCost'] = info['ShippingLabelCost']

    
    for key, value in itemsSold.iteritems():        
        print(key)
        print(value)

            
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
# http://www.tutorialspoint.com/python/string_find.htm
