from ebaysdk.trading import Connection as Trading
from ShippingInfoModule import ShippingInfoClass
from ItemsHeldModule import ItemsHeldClass
import json, re
from pathFunction import resource_path

class ItemInfoClass:

    def __init__(self, json_fileName_iic="ItemInfo.json", ids=None,
                 json_fileName_sic="ShippingInfo.json", shippingHTMLFile="My eBay.html",
                 json_fileName_ihc="ItemsHeld.json", user=""
    ):
        """
        - initializes ItemInfoClass
        - requires underlying json file name and
        ids required for access ebay API
        """
        self.json_fileName_iic = resource_path(json_fileName_iic)
        self.json_fileName_ihc = resource_path(json_fileName_ihc)
        self.json_fileName_sic = resource_path(json_fileName_sic)
        self.shippingHTMLFile = shippingHTMLFile
        self.user = user
        self._ItemsSold = None
        if ids is None:
            print("No ids")
            return
        self.api = Trading(appid=ids[0], devid=ids[1], certid=ids[2],
                           token=ids[3], config_file=None)
        try:
            fileHandler = open(self.json_fileName_iic, 'r')
            self._ItemsSold = json.load(fileHandler)
            fileHandler.close()
        except:
            self._ItemsSold = {
                self.user:{}
            }

        self.recordedItems = {} # holds recorded items
        self.unrecordedItems = {} # holds unrecorded items
        self.requestedItemsSold = {} # holds the items that are
                                     # found in the last 'days'

    def get_all_records(self):
        self.requestedItems = None
        return self._format_items_sorted_by_date()


    def get_entry(self, orderID):
        return self._ItemsSold[self.user].get(orderID, "")

    def add_entry(self, orderID, itemInfo_dict):
        self._ItemsSold[self.user][orderID] = itemInfo_dict
        self._update_json_file()

    def delete_entry(self, orderID):
        if self._ItemsSold[self.user].pop(orderID, None) is None:
            # item not found (and not removed)
            # thus we dont need to update json file
            return
        else:
            self._update_json_file()

    def _update_json_file(self):
        """
        updates the underlying json file with the
        records currently held in the _ItemsSold variable.
        """
        fileHandler = open(self.json_fileName_iic, 'w')
        json.dump(self._ItemsSold, fileHandler, indent=2)
        fileHandler.close()


    def _get_new_items_orderID(self):
        """
        - gets the items sold in the last 'days'
        - populates dictionaries self.recordedItems &
        self.unrecordedItems accordingly
        """
        HasMorePages = True
        pageNumber = 1

        while HasMorePages:
            response = self.api.execute('GetMyeBaySelling',
                                        {
                                            'SoldList':
                                            {
                                                'DurationInDays': self.days,
                                                'Pagination':
                                                {
                                                    'EntriesPerPage': 200,
                                                    'PageNumber': pageNumber,
                                                }
                                            }
                                        }
                                    )
            soldListDict = response.dict()['SoldList']
            numberOfPagesDict = soldListDict['PaginationResult']
            numberOfPages = int(numberOfPagesDict['TotalNumberOfPages'])
            if pageNumber < numberOfPages:
                pageNumber = pageNumber + 1 # increase page for next api request
            else:
                HasMorePages = False

            transactionsDict = soldListDict['OrderTransactionArray']
            transactions = transactionsDict['OrderTransaction']
            recorded_keys = self._ItemsSold[self.user].keys()
            for transaction in transactions:
                orderId = transaction['Transaction']['OrderLineItemID']
                # total new items sold = recordedItems + unrecordedItems
                if orderId in recorded_keys:
                    self.recordedItems[orderId] = self._ItemsSold[self.user][orderId]
                else:
                    self.unrecordedItems[orderId] = {}

        print("Total of %s items sold in the last %d days." % (
            numberOfPagesDict['TotalNumberOfEntries'],int(self.days)
        ))



    def _get_new_items_info(self):
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
                                    'NumberOfDays': self.days,
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
            self._append_shipping_info_to_records(self.unrecordedItems)

    def _append_shipping_info_to_records(self, recordsWithoutShippingInfo):
        """
        - appends shipping info to records
        based on the item tracking number
        each record should have.
        """
        orderIDs = recordsWithoutShippingInfo.keys()
        si = ShippingInfoClass(self.json_fileName_sic, self.shippingHTMLFile)

        for orderID in orderIDs:
            tracking_numbers = recordsWithoutShippingInfo[orderID].get('ItemTrackingNumber', [])
            #print(tracking_numbers)
            tracking_numbers_dict = {}
            for tracking_number in tracking_numbers:
                info = si.getLabelInfo(tracking_number)
                if info is not None and "Void" not in info['ShippingStatus']:
                    tracking_numbers_dict[float(info['ShippingLabelCost'][1:])]={
                        'ShippingLabelCost': info['ShippingLabelCost'],
                        'BuyerName': info['BuyerName'],
                        'ShippingStatus': info['ShippingStatus']
                    }
            if len(tracking_numbers_dict.keys()) > 1:
                highest_price = max(tracking_numbers_dict.keys())
                recordsWithoutShippingInfo[orderID]['ShippingStatus'] = (
                    tracking_numbers_dict[highest_price]['ShippingStatus']
                )
                recordsWithoutShippingInfo[orderID]['BuyerName'] = (
                    tracking_numbers_dict[highest_price]['BuyerName']
                )
                recordsWithoutShippingInfo[orderID]['ShippingLabelCost']= (
                    tracking_numbers_dict[highest_price]['ShippingLabelCost']
                )
            elif len(tracking_numbers_dict.keys()) == 1:
                highest_price = tracking_numbers_dict.keys()[0]
                recordsWithoutShippingInfo[orderID]['ShippingStatus'] = (
                    tracking_numbers_dict[highest_price]['ShippingStatus']
                )
                recordsWithoutShippingInfo[orderID]['BuyerName'] = (
                    tracking_numbers_dict[highest_price]['BuyerName']
                )
                recordsWithoutShippingInfo[orderID]['ShippingLabelCost']= (
                    tracking_numbers_dict[highest_price]['ShippingLabelCost']
                )
            else:
                print("Shipping Label Info Not Found")


    def refresh_records_held(self):
        """
        updates records we have with
        the name and shipping info
        in case we update name or shipping
        info later
        """
        self._append_shipping_info_to_records(self._ItemsSold[self.user])
        self._append_name_info_to_records(self._ItemsSold[self.user])
        self._update_json_file()

    def get_new_items_sold(self, days):
        """
        function meant to be used by developers using the class
        - requires days as an argument (string or int) which
        represents the number of days in the past one requires
        the items sold.
        """
        self.days = days
        self._get_new_items_orderID()

        unrecordedOrderIDList = self.unrecordedItems.keys()
        # unrecordedOrderIDList consists of the order ID of
        # the items sold, remove the order item
        # ids that we already have records for
        # in the json file to reduce operation time

        if len(unrecordedOrderIDList) > 0:
            # updating required
            # we have items with incomplete
            # item records
            self._get_new_items_info()

        # before adding new items to records,
        # append name info
        self._append_name_info_to_records(self.unrecordedItems)
        self._append_name_info_to_records(self.recordedItems)
        # add new unrecorded items to the record
        self._ItemsSold[self.user].update(self.unrecordedItems)
        self._update_json_file()
        # requestedItems will be all the items
        # that are found to be sold in the
        # 'days' as specified

        # it will consist of the both recorded
        # and unrecorded items.
        self.requestedItemsSold.update(self.unrecordedItems)
        self.requestedItemsSold.update(self.recordedItems)

        return self._format_items_sorted_by_date()
        # for key, value in self.requestedItemsSold.iteritems():
        #     print(key)
        #     print(value)

    def _append_name_info_to_records(self, records):
        """
        Adds entries for long_name,
        short_name and cost_of_item
        taken from items held records.
        Operates on requestedItems only

        Return not required
        """
        ihc = ItemsHeldClass(self.json_fileName_ihc)
        itemsHeld = ihc.ItemsHeld
        for key, value in records.iteritems():
            # convert long name to short name
            # if available
            long_name = value['ItemName'].replace(" ","")
            value['cost_of_item'] = '0'
            if itemsHeld.get(long_name, None) is not None:
                value['ItemName'] = itemsHeld[long_name].get('short_name', value['ItemName'])
                value['cost_of_item'] = itemsHeld[long_name].get('cost_of_item')


    def _format_items_sorted_by_date(self):
        """
        returns a dictionary of the
        items with date of transaction
        as the key
        """
        working_dict = {}
        items_sold_by_date = {}
        if self.requestedItemsSold:
            working_dict = self.requestedItemsSold
        else:
            working_dict = self._ItemsSold[self.user]

        for orderID, item_record in working_dict.iteritems():
            if item_record.get('ItemDate', False):
                items_sold_by_date[item_record['ItemDate']] = item_record
                del items_sold_by_date[item_record['ItemDate']]['ItemDate']
        return items_sold_by_date


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
