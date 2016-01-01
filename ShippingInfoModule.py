from bs4 import BeautifulSoup
from constants import shippingInfo, targetHtmlFile
import os, re, json


class ShippingInfoClass:
    
    def __init__(self, json_fileName):
        self.json_fileName = json_fileName
        fileHandler = open(self.json_fileName, 'r')
        self.ShippingInfo = json.load(fileHandler)
        fileHandler.close()
        self.last_files_time_last_modified = \
                        self.ShippingInfo["update_file"]["time_last_modified"]
        self.last_files_size = \
                        self.ShippingInfo["update_file"]["file_size"]

    def update_json_file(self):
        """
        update main json file by
        overwriting its contents
        with the current contents
        of self.ShippingInfo.
        Also updates update_file key in 
        the json file.
        """
        fileHandler = open(self.json_fileName, 'w') # overwrite file
        self.ShippingInfo["update_file"]["file_size"] = \
                        str(os.path.getsize(targetHtmlFile))
        self.ShippingInfo["update_file"]["time_last_modified"] = \
                        str(os.path.getmtime(targetHtmlFile))

        self.last_files_time_last_modified = \
                        self.ShippingInfo["update_file"]["time_last_modified"]
        self.last_files_size = \
                        self.ShippingInfo["update_file"]["file_size"]

        
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
        count_before = len(self.ShippingInfo)
        fileHandler = open(targetHtmlFile, "r")
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
            self.ShippingInfo[tracking_number] = {"ShippingLabelCost" 
                                                  : shipping_label_cost, 
                                                "ShippingStatus": 
                                                  shipping_status, 
                                                "BuyerName" : 
                                                  name}
        count_after = len(self.ShippingInfo)
        print("Count before: %d and after: %d, resulting in an increase of %d entries/entry." %(count_before, count_after, count_after-count_before))
        self.update_json_file()

            
        
    #print(shippingInfo)
    #print(shippingInfo["millerbritt"]["ShippingLabelCost"])

    def getLabelInfo(self, key):
        result = self.ShippingInfo.get(key, None)
        if result is not None:
            # if key is found
            # return the result
            return result 

        # if not, see if we can update
        # the ShippingInfo variable
        if self.shouldWeUpdate():
            self.update_ShippingInfo_and_file()
            # return the result
            # from the updated
            # ShippingInfo. If 
            # still not present, 
            # it is not created...
            return self.ShippingInfo.get(key, None)
            

    def shouldWeUpdate(self):
        """
        check if 
        """
        # http://stackoverflow.com/questions/6591931/getting-file-size-in-python
        # http://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
        current_files_time_last_modified = os.path.getmtime(targetHtmlFile)
        current_files_size = os.path.getsize(targetHtmlFile)
        if str(current_files_time_last_modified) == self.last_files_time_last_modified and str(current_files_size) == self.last_files_size:
            #print("Can NOT update")
            return False
        else:
            print("Can update, updating!!!")
            return True


# refs
# https://docs.python.org/2/tutorial/classes.html
# http://www.tutorialspoint.com/python/python_files_io.htm
# http://www.diveintopython3.net/serializing.html   
