import unittest, os
from ShippingInfoModule import ShippingInfoClass

json_fileName = "ShippingInfoClassTest.json"
class ShippingInfoClassTest(unittest.TestCase):

    def setUp(self):
        # create object
        self.sic = ShippingInfoClass(json_fileName)

    def tearDown(self):
        # nullify object
        # and delete record folder
        self.sic = None
        os.remove(json_fileName)

    def test_add_entry(self):
        self.sic.add_entry("some keys", "shipping info")
        self.assertTrue(
            self.sic.get_shipping_info("some keys") == "shipping info"
        )

    def test_delete_entry(self):
        self.sic.add_entry("some keys", "shipping info")
        self.assertTrue(
            self.sic.get_shipping_info("some keys") == "shipping info"
        )
        self.sic.delete_entry("some keys")
        self.assertTrue(
            self.sic.get_shipping_info("some keys") == ""
        )


if __name__ == '__main__':
    unittest.main()
