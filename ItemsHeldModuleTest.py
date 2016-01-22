import unittest, os
from ItemsHeldModule import ItemsHeldClass

json_fileName = "ItemsHeldClassTest.json"
items_held_entry = {
    "long_name": "long name @#",
    "short_name": "short 23 12",
    "cost_of_item": "39942.23"
}
class ItemsHeldClassTest(unittest.TestCase):

    def setUp(self):
        # create object
        self.ihc = ItemsHeldClass(json_fileName)


    def tearDown(self):
        # nullify object
        # and delete record folder
        self.ihc = None
        os.remove(json_fileName)

    def test_add_entry(self):
        self.ihc.add_entry(
            items_held_entry["long_name"],
            items_held_entry["short_name"],
            items_held_entry["cost_of_item"],
        )
        short_name = self.ihc.get_short_name(
            items_held_entry['long_name']
        )
        cost_of_item = self.ihc.get_cost_of_item(
            items_held_entry['long_name']
        )
        self.assertTrue(
            short_name is items_held_entry['short_name']
            and
            cost_of_item is items_held_entry['cost_of_item']
        )

    def test_delete_entry(self):
        self.ihc.add_entry(
            items_held_entry["long_name"],
            items_held_entry["short_name"],
            items_held_entry["cost_of_item"],
        )
        self.ihc.delete_entry(items_held_entry["long_name"])
        short_name = self.ihc.get_short_name(
            items_held_entry['long_name']
        )
        cost_of_item = self.ihc.get_cost_of_item(
            items_held_entry['long_name']
        )
        self.assertTrue(
            short_name is ""
            and
            cost_of_item is ""
        )

    def test_updating_records_with_file(self):
        testFile = "testFile.txt"
        testValues = [
            [
                "long boring name... ",
                " short fun name! ",
                "32",
            ],
            [
                "long boring name2... ",
                " short fun name2! ",
                "32.2",
            ],
        ]
        fileHandler = open(testFile, 'w')
        for testValue in testValues:
            output = (
                testValue[0] + "\t" +
                testValue[1] + "\t" +
                testValue[2] + "\n"
            )
            fileHandler.write(output)
        fileHandler.close()
        self.ihc.update_ItemsHeld_and_file(testFile)
        for testValue in testValues:
            long_name, short_name, cost_of_item = testValue
            self.assertTrue(
                self.ihc.get_short_name(long_name) == short_name
                and
                self.ihc.get_cost_of_item(long_name) == cost_of_item
            )
        os.remove(testFile)

    def test_differentUsers(self):
        self.ihc_user1 = ItemsHeldClass(json_fileName, user="u1")
        self.ihc_user2 = ItemsHeldClass(json_fileName, user="u2")
        self.ihc_user1.add_entry(
            items_held_entry["long_name"],
            items_held_entry["short_name"],
            items_held_entry["cost_of_item"],
        )
        short_name_u1 = self.ihc_user1.get_short_name(
            items_held_entry['long_name']
        )
        cost_of_item_u1 = self.ihc_user1.get_cost_of_item(
            items_held_entry['long_name']
        )
        short_name_u2 = self.ihc_user2.get_short_name(
            items_held_entry['long_name']
        )
        cost_of_item_u2 = self.ihc_user2.get_cost_of_item(
            items_held_entry['long_name']
        )

        self.assertTrue(
            short_name_u1 is items_held_entry['short_name']
            and
            cost_of_item_u1 is items_held_entry['cost_of_item']
            and
            short_name_u2 is not items_held_entry['short_name']
            and
            cost_of_item_u2 is not items_held_entry['cost_of_item']
        )
if __name__ == '__main__':
    unittest.main()

# ref:
# http://stackoverflow.com/questions/6996603/how-do-i-delete-a-file-or-folder-in-python
