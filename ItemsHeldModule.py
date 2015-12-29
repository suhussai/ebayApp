import json

class ItemsHeldClass:
    
    def __init__(self, json_fileName):
        self.json_fileName = json_fileName
        fileHandler = open(self.json_fileName, 'r')
        self.ItemsHeld = json.load(fileHandler)
        fileHandler.close()
        
    def get_short_name(self, long_name):
        value = self.ItemsHeld.get(long_name, None)
        if value is not None:
            return value.get("short_name", "")
        else:
            return ""

    def get_cost_of_item(self, long_name):
        value = self.ItemsHeld.get(long_name, None)
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
                self.ItemsHeld[long_name.replace(" ","")] = {'long_name': long_name,
                                                   'short_name': short_name,
                                             'cost_of_item': cost_of_item
                                        }               
            else:
                print("found problem line " + line)
        s = 'TWO WHEEL CENTER HUB CAPS For 07-15 CADILLAC ESCALADE 22 " PLAIN  CREST  9596649'.replace(" ","")
        print(self.ItemsHeld.get(s), "Nope")
        self.update_json_file()
    

        
        
