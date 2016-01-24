import json, os
from pathFunction import resource_path

class ItemsHeldClass:

    def __init__(self, json_fileName, user="", meipass=""):
        self.meipass = meipass
        self.json_fileName = resource_path(json_fileName, self.meipass)
        print(self.json_fileName)
        self.currentUser = user
        try:
            fileHandler = open(self.json_fileName, 'r')
            self.ItemsHeld = json.load(fileHandler)
            fileHandler.close()
        except:
            self.ItemsHeld = {
                self.currentUser: {}
            }

    def add_entry(self, long_name, short_name, cost_of_item):
        self.get_users_main_record()[long_name.replace(" ","")] = {
            'long_name': long_name,
            'short_name': short_name,
            'cost_of_item': cost_of_item
        }
        self.update_json_file()

    def refresh_record(self):
        """
        reread record from file
        """
        try:
            fileHandler = open(self.json_fileName, 'r')
            self.ItemsHeld = json.load(fileHandler)
            fileHandler.close()
        except:
            self.ItemsHeld = {
                self.currentUser: {}
            }

    def get_users_main_record(self):
        if self.ItemsHeld.get(self.currentUser, None) is None:
            self.ItemsHeld[self.currentUser] = {}
        return self.ItemsHeld[self.currentUser]

    def get_records(self):
        return self.get_users_main_record()

    def delete_entry(self, long_name):
        self.get_users_main_record().pop(long_name.replace(" ", ""), None)
        self.update_json_file()
    def get_short_name(self, long_name):
        value = self.get_users_main_record().get(long_name.replace(" ", ""), None)
        if value is not None:
            return value.get("short_name", "")
        else:
            return ""

    def get_cost_of_item(self, long_name):
        value = self.get_users_main_record().get(long_name.replace(" ", ""), None)
        if value is not None:
            return value.get("cost_of_item", "")
        else:
            return ""

    def update_json_file(self):
        fileHandler = open(self.json_fileName, 'w')
        json.dump(self.ItemsHeld, fileHandler, indent=2)
        fileHandler.close()


    def update_ItemsHeld_and_file(self, update_file):
        # 4x Wheel Center Hub Caps FOR Tacoma and 4Runner (1996-2002) 15"/16" Rims, 6 lugs\t4 pcs tundra caps\t$10.00\n
        update_fileHandler = open(update_file, 'r')
        content = update_fileHandler.read()

        for line in content.split('\n'):
            values = line.split('\t')
            if len(values) == 3:
                long_name = values[0]
                short_name = values[1]
                cost_of_item = values[2]
                self.get_users_main_record()[long_name.replace(" ","")] = {
                    'long_name': long_name,
                    'short_name': short_name,
                    'cost_of_item': cost_of_item
                }
            else:
                print("Error with line: " + line)
        self.update_json_file()




