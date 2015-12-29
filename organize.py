from ItemInfoModule import ItemInfoClass
from ItemsHeldModule import ItemsHeldClass
ihc = ItemsHeldClass("ItemsHeld.json")
itemsHeld = ihc.ItemsHeld
iic = ItemInfoClass("ItemInfo.json")
itemsSold = iic.ItemsSold

for key, value in itemsSold.iteritems():
    # convert long name to short name
    # if available
    long_name = value['ItemName'].replace(" ","")
    if itemsHeld.get(long_name, None) is not None:        
        value['ItemName'] = itemsHeld[long_name].get('short_name', long_name)
        value['cost_of_item'] = itemsHeld[long_name].get('cost_of_item', '0.0')
    else:
        value['Name'] = long_name
        value['cost_of_item'] = '0.0'
        

itemsSoldDated = {}
for key, value in itemsSold.iteritems():
    if value.get('ItemDate', None) is None:
        continue
    itemsSoldDated[value['ItemDate']] = value
    del itemsSoldDated[value['ItemDate']]['ItemDate']


print("Displaying-------------")
itemsSoldDatedList = sorted(itemsSoldDated.items())

for itemsSold in itemsSoldDatedList:
    print(itemsSold)
