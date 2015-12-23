from bs4 import BeautifulSoup
import re

fileHandler = open("target.html", "r")
data = fileHandler.read()
fileHandler.close()

soup = BeautifulSoup(data, "html.parser")
rows = soup.find_all('table')
shippingInfo = {}
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
    shippingInfo[name] = {"ShippingLabelCost" : shipping_label_cost, 
                          "ShippingStatus": shipping_status, 
                          "TrackingNumber" :tracking_number}

print(shippingInfo)
#print(shippingInfo["millerbritt"]["ShippingLabelCost"])
