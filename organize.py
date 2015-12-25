from getItemInfo import itemsSold


itemsSoldDated = {}
for key, value in itemsSold.iteritems():
    itemsSoldDated[value['ItemDate']] = value
    del itemsSoldDated[value['ItemDate']]['ItemDate']


print("Displaying-------------")
itemsSoldDatedList = sorted(itemsSoldDated.items())

for itemsSold in itemsSoldDatedList:
    print(itemsSold)
