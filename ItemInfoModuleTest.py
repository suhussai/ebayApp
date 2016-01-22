import unittest, os
from ItemInfoModule import ItemInfoClass
from ShippingInfoModule import ShippingInfoClass

json_fileName_iic = "ItemInfoClassTest.json"
json_fileName_sic = "ShippingInfoClassTest.json"

class ShippingInfoClassTest(unittest.TestCase):

    def setUp(self):
        # create object
        self.iic = ItemInfoClass(json_fileName_iic, ids="Not None", json_fileName_sic=json_fileName_sic)

    def tearDown(self):
        # nullify object
        # and delete record folder
        self.iic = None
        os.remove(json_fileName_iic)

    def test_refresh(self):
        self.iic.add_entry(
            "funkyOrderID",
            {
                "ItemPrice": "49.99",
                "ItemTrackingNumber": [
                    "938097482334"
                ],
                "ItemName": "TWO CREST  9596649",
                "cost_of_item": "N/A",
                "ItemDate": "2016-01-11T24:26:03.000Z"
            }
        )
        self.sic = ShippingInfoClass(json_fileName_sic)
        self.sic.add_entry(
            "938097482334",
            {
                'ShippingLabelCost': "4.32",
                'BuyerName': "Joe Boxer",
                'ShippingStatus': "MIA"
            }
        )
        self.assertTrue(
            self.iic.get_entry("funkyOrderID").get('ShippingLabelCost', None) is not "4.32"
        )

        self.iic.refresh_records_held()

#        print(self.iic.get_entry("funkyOrderID"))
#        print(self.sic.ShippingInfo)
        self.assertTrue(
            self.iic.get_entry("funkyOrderID").get('ShippingLabelCost', None) == "4.32"
        )

        self.sic = None
        os.remove(json_fileName_sic)

    def test_differentUsers(self):
        self.iic_user1 = ItemInfoClass(json_fileName_iic,
                                       ids="Not None",user="u1",
                                       json_fileName_sic=json_fileName_sic)
        self.iic_user2 = ItemInfoClass(json_fileName_iic,
                                    ids="Not None",user="u2",
                                    json_fileName_sic=json_fileName_sic)
        self.iic_user1.add_entry("key1", "value1")
        self.assertTrue(
            self.iic_user1.get_entry("key1") == "value1"
            and
            self.iic_user2.get_entry("key1") == ""
        )
        self.iic_user1 = None
        self.iic_user2 = None

if __name__ == '__main__':
    unittest.main()
