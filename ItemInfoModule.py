from ebaysdk.trading import Connection as Trading
from ShippingInfoModule import ShippingInfoClass
from constants import days, ids
import json, re

class ItemInfoClass:
    
    def __init__(self, json_fileName):
        self.json_fileName = json_fileName
        fileHandler = open(self.json_fileName, 'r')
        self.api = Trading(appid=ids[0], devid=ids[1], certid=ids[2], token=ids[3])
        self._ItemsSold = json.load(fileHandler)
        fileHandler.close()        
        self.si = ShippingInfoClass('ShippingInfo.json')
        self.recordedItems = {} # holds recorded items
        self.unrecordedItems = {} # holds unrecorded items
        self.requestedItemsSold = {} # holds the items that are 
                                     # found in the last 'days'
    def update_json_file(self):
        fileHandler = open(self.json_fileName, 'w')
        json.dump(self._ItemsSold, fileHandler, indent=2)
        fileHandler.close()


    def get_new_items_orderID(self):
        """
        - gets the items sold in the last 'days'
        - populates dictionaries self.recordedItems & self.unrecordedItems 
        accordingly
        """
        HasMorePages = True
        pageNumber = 1
        orderIDList = []
        newItemsSold = {}

        while HasMorePages:
            response = self.api.execute('GetMyeBaySelling', 
                                   {'SoldList': 
                                    {'DurationInDays' : days,
                                     'Pagination': {'EntriesPerPage': 200,
                                                    'PageNumber': pageNumber}}
                                }
            )
            if pageNumber < int(response.dict()['SoldList']['PaginationResult']['TotalNumberOfPages']):
                pageNumber = pageNumber + 1 # increase page for next api request
            else:
                HasMorePages = False
            recorded_keys = self._ItemsSold.keys()
            for transaction in response.dict()['SoldList']['OrderTransactionArray']['OrderTransaction']:
                orderId = transaction['Transaction']['OrderLineItemID']
                # total new items sold = recordedItems + unrecordedItems
                if orderId in recorded_keys:
                    self.recordedItems[orderId] = self._ItemsSold[orderId]
                else:
                    #orderIDList.append(orderId)
                    self.unrecordedItems[orderId] = {}
                    # else:
                    #     print(str(orderId) + " already recorded in:" +  str(recorded_keys))
        print("Total of %s items sold in the last %d days." % (int(response.dict()['SoldList']['PaginationResult']['TotalNumberOfEntries']), int(days)))
        
    
    def get_new_items_info(self):
        """
        - looks through ebay orders for 
        all items for which we have no
        information on record
        - populates unrecorded item infos
        that have no item info with item info
        """
        HasMoreOrders = True
        pageNumber = 0
        while (HasMoreOrders):
            pageNumber = pageNumber + 1
            #print("Reading page " + str(pageNumber))
            response = self.api.execute('GetOrders',
                                   {'OrderIDArray': {'OrderID': self.unrecordedItems.keys()},
                                    'NumberOfDays': days,
                                    'Pagination' : {'EntriesPerPage': 100, 'PageNumber': pageNumber}}
            )
            if 'false' in response.dict()['HasMoreOrders']:
                HasMoreOrders = False
            else:
                HasMoreOrders = True

            #unrecordedOrderIDList = ['252139120978-1743240659015']
            #print("Response for " + str(len(response.dict()['OrderArray']['Order'])) + " order IDs")
            for order in response.dict()['OrderArray']['Order']:
                # get basic information for each
                # of the items sold
                orderID = order['OrderID'] 
                #if orderID in self.unrecordedItems.keys():
                for transaction in order['TransactionArray']['Transaction']: 
                    item_name = transaction['Item']['Title']
                    item_tracking_number = []
                    if transaction['ShippingDetails'].get('ShipmentTrackingDetails', None) is not None:
                        shipping_details = transaction['ShippingDetails']['ShipmentTrackingDetails']

                        if type(shipping_details) is not  list:
                            shipping_details = [shipping_details]

                        for shipping_detail in shipping_details:
                            item_tracking_number.append(shipping_detail['ShipmentTrackingNumber'])

                    else:
                        print(transaction)
                        print(transaction['ShippingDetails'])
                    
                # add information to the dictionary
                order_date = order['CreatedTime'] # ex: 2015-12-16T21:13:54.000Z
                item_total_price = order['Total']['value']
                self.unrecordedItems[orderID]['ItemName'] = item_name
                self.unrecordedItems[orderID]['ItemPrice'] = item_total_price
                self.unrecordedItems[orderID]['ItemTrackingNumber'] = item_tracking_number
                self.unrecordedItems[orderID]['ItemDate'] = order_date #[:order_date.find("T")]
            

            # attach shipping info 
            # to items
            orderIDs = self.unrecordedItems.keys()
            for orderID in orderIDs:
                tracking_numbers = self.unrecordedItems[orderID].get('ItemTrackingNumber', [])
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
                    self.unrecordedItems[orderID]['ShippingStatus'] = tracking_numbers_dict[highest_price]['ShippingStatus']
                    self.unrecordedItems[orderID]['BuyerName'] = tracking_numbers_dict[highest_price]['BuyerName']
                    self.unrecordedItems[orderID]['ShippingLabelCost'] = tracking_numbers_dict[highest_price]['ShippingLabelCost']            
                elif len(tracking_numbers_dict.keys()) == 1:                    
                    highest_price = tracking_numbers_dict.keys()[0]
                    self.unrecordedItems[orderID]['ShippingStatus'] = tracking_numbers_dict[highest_price]['ShippingStatus']
                    self.unrecordedItems[orderID]['BuyerName'] = tracking_numbers_dict[highest_price]['BuyerName']
                    self.unrecordedItems[orderID]['ShippingLabelCost'] = tracking_numbers_dict[highest_price]['ShippingLabelCost']            
                else:
                    print("Shipping Label Info Not Found") 


    def get_new_items_sold(self):
        
        self.get_new_items_orderID()

        unrecordedOrderIDList = self.unrecordedItems.keys()
        #print("Total of %s items sold in the last %d days." % (int(response.dict()['SoldList']['PaginationResult']['TotalNumberOfEntries']), int(days)))
        # unrecordedOrderIDList consists of the order ID of 
        # the items sold, remove the order item 
        # ids that we already have records for
        # in the json file to reduce operation time

                
        if len(unrecordedOrderIDList) > 0:
            # updating required
            # we have items with incomplete
            # item records
            self.get_new_items_info()
            
        #print(self.unrecordedItems)
        # add new unrecorded items to the record
        self._ItemsSold.update(self.unrecordedItems)

        self.update_json_file()
        # requestedItems will be all the items
        # that are found to be sold in the 
        # 'days' as specified

        # it will consist of the both recorded
        # and unrecorded items.
        self.requestedItemsSold.update(self.unrecordedItems) 
        self.requestedItemsSold.update(self.recordedItems)
        # for key, value in self.requestedItemsSold.iteritems():        
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
