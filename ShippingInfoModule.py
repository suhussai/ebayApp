from bs4 import BeautifulSoup
#from constants import shippingInfo, targetHtmlFile
import os, re, json
from pathFunction import resource_path


class ShippingInfoClass:

    def __init__(self, json_fileName="ShippingInfo.json",
                 targetHtmlFile="My eBay.html",
                 user=""):
        """
        initializing function
        - requires the underlying json file record
        - requires targetHtmlFile where the shipping info,
        mainly the shipping cost, will be 'web crawled' out.
        """
        self.json_fileName = resource_path(json_fileName)
        self.targetHtmlFile = targetHtmlFile
        self.currentUser = user
        self.ShippingInfo = {
            self.currentUser: {}
        }
        try:
            fileHandler = open(self.json_fileName, 'r')
            self.ShippingInfo = json.load(fileHandler)
            fileHandler.close()
        except:
            self.ShippingInfo[self.currentUser] = {
                "update_file": {
                    "time_last_modified" : 0,
                    "file_size" : 0
                }
            }

        self.last_files_time_last_modified = \
                        self.ShippingInfo[self.currentUser]["update_file"]["time_last_modified"]
        self.last_files_size = \
                        self.ShippingInfo[self.currentUser]["update_file"]["file_size"]

    def refresh_record(self):
        """
        reread record from file
        """
        try:
            fileHandler = open(self.json_fileName, 'r')
            self.ShippingInfo = json.load(fileHandler)
            fileHandler.close()
        except:
            self.ShippingInfo[self.currentUser] = {
                "update_file": {
                    "time_last_modified" : 0,
                    "file_size" : 0
                }
            }

    def get_shipping_info(self, key):
        return self.ShippingInfo[self.currentUser].get(key, "")

    def add_entry(self, key, value):
        self.ShippingInfo[self.currentUser][key] = value
        self._update_json_file()

    def delete_entry(self, key):
        if self.ShippingInfo[self.currentUser].pop(key, None) is None:
            # item not found (and not removed)
            # thus we dont need to update json file
            return
        else:
            self._update_json_file()

    def _update_json_file(self):
        """
        update main json file by
        overwriting its contents
        with the current contents
        of self.ShippingInfo.
        Also updates update_file key in
        the json file.
        """
        try:
            file_size = str(os.path.getsize(self.targetHtmlFile))
            file_time_modified = str(os.path.getmtime(self.targetHtmlFile))
        except:
            file_size = str(0)
            file_time_modified = str(0)

        fileHandler = open(self.json_fileName, 'w') # overwrite file
        self.ShippingInfo[self.currentUser]["update_file"]["file_size"] = file_size

        self.ShippingInfo[self.currentUser]["update_file"]["time_last_modified"] = file_time_modified


        self.last_files_time_last_modified = \
                        self.ShippingInfo[self.currentUser]["update_file"]["time_last_modified"]
        self.last_files_size = \
                        self.ShippingInfo[self.currentUser]["update_file"]["file_size"]


        json.dump(self.ShippingInfo, fileHandler, indent=2)
        fileHandler.close()

    def update_ShippingInfo_and_file(self):
        """
        Assumes targetHtmlFile is the
        file name of the shipping label
        page found on my ebay.
        Reads contents for
        information on the items
        and especially shipping label
        cost and item status.
        """
        count_before = len(self.ShippingInfo[self.currentUser])
        fileHandler = open(self.targetHtmlFile, "r")
        data = fileHandler.read()
        fileHandler.close()
        soup = BeautifulSoup(data, "html.parser")
        rows = soup.find_all('table')
        #shippingInfo = {}
        i = 0
        shippingInfoRow = rows[5].find_all('div')
        regexComp = re.compile('\d+')
        while (i < len(shippingInfoRow)):
            name = shippingInfoRow[i + 1].get_text().split()[0]
            shipping_label_cost = shippingInfoRow[i + 2].get_text()
            status_and_number = shippingInfoRow[i + 5].get_text()
            regexCompResult = regexComp.search(status_and_number)
            shipping_status, tracking_number = (
                status_and_number[:regexCompResult.span()[0]-1],
                status_and_number[regexCompResult.span()[0]:
                                  regexCompResult.span()[1]]
            )
            i = i + 9
            self.ShippingInfo[self.currentUser][tracking_number] = {"ShippingLabelCost"
                                                  : shipping_label_cost,
                                                "ShippingStatus":
                                                  shipping_status,
                                                "BuyerName" :
                                                  name}
        count_after = len(self.ShippingInfo[self.currentUser])
        print("Count before: %d and after: %d, resulting in an increase of %d entries/entry." %(count_before, count_after, count_after-count_before))
        self._update_json_file()


    #print(shippingInfo)
    #print(shippingInfo["millerbritt"]["ShippingLabelCost"])

    def getLabelInfo(self, key):
        """
        returns label info for key.
        arguments:
        key: is the item tracking number
        for which we will check if we have
        shipping info for.
        If item tracking number doesn't exist,
        the function will check if we need to
        update, and will do so if necessary.
        """
        result = self.ShippingInfo[self.currentUser].get(key, None)
        if result is not None:
            # if key is found
            # return the result
            return result

        # if not, see if we can update
        # the ShippingInfo variable
        if self._shouldWeUpdate():
            self.update_ShippingInfo_and_file()
            # return the result
            # from the updated
            # ShippingInfo. If
            # still not present,
            # it is not created...
            return self.ShippingInfo[self.currentUser].get(key, None)

    def _shouldWeUpdate(self):
        """
        check if we need to update shipping info.
        Criteria (Update if:):
        - we have a newer file
        - we have a bigger file
        """
        # http://stackoverflow.com/questions/6591931/getting-file-size-in-python
        # http://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
        try:
            current_files_time_last_modified = os.path.getmtime(self.targetHtmlFile)
            current_files_size = os.path.getsize(self.targetHtmlFile)
            if str(current_files_time_last_modified) == self.last_files_time_last_modified and str(current_files_size) == self.last_files_size:
                #print("Can NOT update")
                return False
            else:
                print("Can update, updating!!!")
            return True
        except Exception as e:
            # likely couldn't find file
            print(e)
            return False

# refs
# https://docs.python.org/2/tutorial/classes.html
# http://www.tutorialspoint.com/python/python_files_io.htm
# http://www.diveintopython3.net/serializing.html
