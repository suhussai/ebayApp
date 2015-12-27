from ItemInfoModule import ItemInfoClass

iic = ItemInfoClass("ItemInfo.json")
iic.get_new_items_sold()

for key, value in iic.ItemsSold.iteritems():
    print(key)
    print(value)
    print("----------------------------------")
