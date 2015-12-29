from ebaysdk.trading import Connection as Trading
from ShippingInfoModule import ShippingInfoClass
from constants import days, ids
import json, re

class ItemInfoClass:
    
    def __init__(self, json_fileName):
        self.json_fileName = json_fileName
        fileHandler = open(self.json_fileName, 'r')
        self.ItemsSold = json.load(fileHandler)
        fileHandler.close()        
        self.si = ShippingInfoClass('ShippingInfo.json')

    def update_json_file(self):
        fileHandler = open(self.json_fileName, 'w')
        json.dump(self.ItemsSold, fileHandler, indent=2)
        fileHandler.close()
        
        
    def get_new_items_sold(self):
        api = Trading(appid=ids[0], devid=ids[1], certid=ids[2], token=ids[3])
        response = api.execute('GetMyeBaySelling', 
                               {'SoldList': 
                                {'DurationInDays' : days} 
                            }
                           )
        orderIDList = []
        newItemsSold = {}
        recorded_keys = self.ItemsSold.keys()
        for transaction in response.dict()['SoldList']['OrderTransactionArray']['OrderTransaction']:
            orderId = transaction['Transaction']['OrderLineItemID']
            if orderId not in recorded_keys:
                orderIDList.append(orderId)
                newItemsSold[orderId] = self.ItemsSold.get(orderId, {})
            # else:
            #     print(str(orderId) + " already recorded in:" +  str(recorded_keys))
            
                
        #print("Found " + str(len(orderIDList)) + " new items.")
        # orderIDList consists of the order ID of 
        # the items sold, remove the order item 
        # ids that we already have records for
        # in the json file to reduce operation time

                
        if len(orderIDList) == 0:
            # no updating required
            # we have up to date
            # item records
            return
            
        HasMoreOrders = True
        pageNumber = 0
        while (HasMoreOrders):
            pageNumber = pageNumber + 1
            #print("Reading page " + str(pageNumber))
            response = api.execute('GetOrders',
                                   {'OrderIDArray': {'OrderID': orderIDList},
                                    'NumberOfDays': days,
                                    'Pagination' : {'EntriesPerPage': 100, 'PageNumber': pageNumber}}
            )
            if 'false' in response.dict()['HasMoreOrders']:
                HasMoreOrders = False
            else:
                HasMoreOrders = True

            #orderIDList = ['252139120978-1743240659015']
            #print("Response for " + str(len(response.dict()['OrderArray']['Order'])) + " order IDs")
            for order in response.dict()['OrderArray']['Order']:
                orderID = order['OrderID'] 
                #if orderID in newItemsSold.keys():
                for transaction in order['TransactionArray']['Transaction']: 
                    item_name = transaction['Item']['Title']
                    shipping_details = transaction['ShippingDetails']['ShipmentTrackingDetails']
                    item_tracking_number = []

                    if type(shipping_details) is not  list:
                        shipping_details = [shipping_details]

                    for shipping_detail in shipping_details:
                        item_tracking_number.append(shipping_detail['ShipmentTrackingNumber'])

                order_date = order['CreatedTime'] # ex: 2015-12-16T21:13:54.000Z
                item_total_price = order['Total']['value']
                newItemsSold[orderID]['ItemName'] = item_name
                newItemsSold[orderID]['ItemPrice'] = item_total_price
                newItemsSold[orderID]['ItemTrackingNumber'] = item_tracking_number
                newItemsSold[orderID]['ItemDate'] = order_date #[:order_date.find("T")]
            
            orderIDs = newItemsSold.keys()
            for orderID in orderIDs:
                tracking_numbers = newItemsSold[orderID].get('ItemTrackingNumber', [])
                #print(tracking_numbers)
                tracking_numbers_dict = {}
                for tracking_number in tracking_numbers:
                    info = self.si.getLabelInfo(tracking_number)
                    if info is not None and "Void" not in info['ShippingStatus']:
                        tracking_numbers_dict[float(info['ShippingLabelCost'][1:])] = {'ShippingLabelCost': info['ShippingLabelCost'],
                                                                            'BuyerName': info['BuyerName'],
                                                                            'ShippingStatus': info['ShippingStatus']
                        }
                if len(tracking_numbers_dict.keys()) > 1:
                    highest_price = max(tracking_numbers_dict.keys())
                    newItemsSold[orderID]['ShippingStatus'] = tracking_numbers_dict[highest_price]['ShippingStatus']
                    newItemsSold[orderID]['BuyerName'] = tracking_numbers_dict[highest_price]['BuyerName']
                    newItemsSold[orderID]['ShippingLabelCost'] = tracking_numbers_dict[highest_price]['ShippingLabelCost']            
                elif len(tracking_numbers_dict.keys()) == 1:                    
                    highest_price = tracking_numbers_dict.keys()[0]
                    newItemsSold[orderID]['ShippingStatus'] = tracking_numbers_dict[highest_price]['ShippingStatus']
                    newItemsSold[orderID]['BuyerName'] = tracking_numbers_dict[highest_price]['BuyerName']
                    newItemsSold[orderID]['ShippingLabelCost'] = tracking_numbers_dict[highest_price]['ShippingLabelCost']            
                else:
                    print("Shipping Label Info Not Found") 
                

        #print(newItemsSold)
        self.ItemsSold.update(newItemsSold)

        self.update_json_file()
    
        # for key, value in self.ItemsSold.iteritems():        
        #     print(key)
        #     print(value)


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
