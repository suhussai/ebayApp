import time
import serial
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, SIGNAL
import sys
import design
import genericDialog
import os
import json
import xlsxwriter
from ItemInfoModule import ItemInfoClass
from ShippingInfoModule import ShippingInfoClass
from ItemsHeldModule import ItemsHeldClass

class genDialog(QtGui.QDialog, genericDialog.Ui_Dialog):
    def __init__(self, textToDisplay="Not Set", parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.labelOutput.setText(textToDisplay)
        self.btnConfirm.clicked.connect(self.closeDialog)

    def closeDialog(self):
        self.done(0)

class eBayApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(eBayApp, self).__init__(parent)
        self.setupUi(self)
        self.ser = None
        self.users = None
        self.currentUser = None
        self.currentUserCredentials = None
        self.itemsHeldClassHandler = ItemsHeldClass("ItemsHeld.json")
        self.display_items_held_tree()
        self.users_file = "users.json"
        self.targetHtmlFile = "target.html"
        try: # in case it doesnt exist
            fileHandler = open(self.users_file, 'r')
            self.users = json.load(fileHandler)
            fileHandler.close()
            self.update_list_user_widget()
        except:
            self.users = {}
        self.btnAddUser.clicked.connect(self.addUser)
        self.btnDeleteUser.clicked.connect(self.deleteUser)
        self.btnSelectAsCurrentUser.clicked.connect(self.selectAsCurrentUser)
        self.btnGetItemsSold.clicked.connect(self.getItemsSold)
        self.btnUpdateShipping.clicked.connect(self.updateShipping)
        self.btnAddNewItem.clicked.connect(self.addNewItem)
        self.btnDeleteItem.clicked.connect(self.deleteItem)
        #self.btnExportToSpreadsheet.clicked.connect(self.exportToSpreadsheet)
        self.btns = [self.btnUpdateShipping, self.btnGetItemsSold,
                     self.btnSelectAsCurrentUser, self.btnDeleteUser,
                     self.btnAddUser]
        #print(self.spinBoxDays.value())

    def deleteItem(self):
        """
        delete item held in items held records
        """
        records_to_be_deleted = self.treeItemsHeld.selectedItems()
        for record in records_to_be_deleted:
            # column zero is long_name
            # followed by short_name
            # and cost_of_item
            long_name = str(record.text(0))
            self.itemsHeldClassHandler.delete_entry(long_name)
        # re-display items that remain
        self.display_items_held_tree()
    def addNewItem(self):
        """
        add new item with:
        - long name from self.lineLongName.text()
        - short name from self.lineShortName.text()
        - cost of item from self.spinCostOfItem.value()
        Note: quick process, separate thread not required
        """
        long_name = str(self.lineLongName.text())
        short_name = str(self.lineShortName.text())
        cost_of_item = str(self.doubleSpinCostOfItem.value())
        self.itemsHeldClassHandler.add_entry(long_name, short_name, cost_of_item)
        formatted_records = [
            long_name,
            short_name,
            cost_of_item
        ]
        # add new item to items held tree
        QtGui.QTreeWidgetItem(self.treeItemsHeld.invisibleRootItem(),
                              formatted_records)

    def updateShipping(self):
        """
        - prepare thread and start
        the thread for the
        update shipping process
        """
        self.setAllButtons(self.btnGetItemsSold, False)
        #days, ids = get_credentials_of_selected_user()
        self.get_thread = updateShippingInfoThread(self.targetHtmlFile)
        self.connect(self.get_thread,
                     SIGNAL('finished_updating_shipping()'),
                     self.finished_getting_items_sold)
        self.get_thread.start()
        print("thread started")

    def setAllButtons(self, exempted_button, state_of_all_other_buttons):
        """
        used for setting all other buttons in gui
        to be True or False except a pre specified btn
        """
        all_other_btns = [btn for btn in self.btns if btn is not exempted_button]
        for btn in all_other_btns:
            btn.setEnabled(state_of_all_other_buttons)

    def finished_updating_shipping(self):
        """
        to be run when the getting new
        update shipping info process is completed
        """
        self.setAllButtons(self.btnUpdateShipping, True) # turn on all buttons
        self.get_thread.terminate()

    def finished_getting_items_sold(self):
        """
        to be run when the getting new
        items sold process is completed
        """
        self.setAllButtons(self.btnGetItemsSold, True) # turn on all buttons
        self.get_thread.terminate()
        self.genDialog = genDialog("Finished Getting Items Sold.\n"
                                   "Exported spreadsheet is ready.")
        self.genDialog.show()

    def get_credentials_of_selected_user(self):
        """
        returns days and ids containing credentials
        in the requried order
        """
        days = int(self.spinBoxDays.value())
        ids = [
            self.currentUserCredentials['AppID'],
            self.currentUserCredentials['DevID'],
            self.currentUserCredentials['CertID'],
            self.currentUserCredentials['TokenID']
        ]
        return ids, days

    def getItemsSold(self):
        self.setAllButtons(self.btnGetItemsSold, False)
        ids, days = self.get_credentials_of_selected_user()

        self.get_thread = getItemsSoldThread(days, ids, "FIXME")
        #self.connect(self.get_thread, SIGNAL('update_items_sold_tree(QString, QString)'), self.update_items_sold_tree)
        self.connect(self.get_thread,
                     SIGNAL('finished_getting_items_sold()'),
                     self.finished_getting_items_sold)

        self.get_thread.start()
        print("thread started")


    def selectAsCurrentUser(self):
        selected_user = self.listUsers.selectedItems()[0]
        print(self.listUsers.selectedItems())
        self.currentUser = str(selected_user.text())
        self.currentUserCredentials = self.users[self.currentUser]
        print(self.currentUser)
        print(self.currentUserCredentials)

    def update_list_user_widget(self):
        self.listUsers.clear()
        for user in self.users.keys():
            self.listUsers.addItem(user)

    def deleteUser(self):
        """
        delete selected user and update list and
        user records
        """
        users_to_be_deleted = self.listUsers.selectedItems()
        for user in users_to_be_deleted:
            self.users.pop(str(user.text()), None)
        self.update_users_file()
        self.update_list_user_widget()

    def addUser(self):
        """
        Adds a new user to the listUsers widget
        and updates the users records file
        - get user name from self.lineUserName.text()
        - get app id from self.lineAppID.text()
        - get cert id from self.lineCertID.text()
        - get dev id from self.lineDevID.text()
        - get token id from self.lineTokenID.text()
        """
        userName = self.lineUserName.text()
        appID = self.lineAppID.text()
        certID = self.lineCertID.text()
        devID = self.lineDevID.text()
        tokenID = self.lineTokenID.text()

        self.users[str(userName)] = {
            "AppID"   : str(appID),
            "CertID"  : str(certID),
            "DevID"   : str(devID),
            "TokenID" : str(tokenID)
        }
        self.update_users_file()
        self.update_list_user_widget()

    def update_users_file(self):
        fileHandler = open(self.users_file, 'w')
        json.dump(self.users, fileHandler, indent=2)
        fileHandler.close()

    def display_items_held_tree(self):
        self.treeItemsHeld.clear()
        item_records = self.itemsHeldClassHandler.ItemsHeld.values()
        item_records.sort()
        # item_records is a list of dicts containing
        # long_name, short_name and cost_of_item
        for items_record in item_records:
            formatted_records = [
                items_record['long_name'],
                items_record['short_name'],
                items_record['cost_of_item']
            ]
            QtGui.QTreeWidgetItem(self.treeItemsHeld.invisibleRootItem(),
                                  formatted_records)

class updateShippingInfoThread(QThread):
    def __init__(self,targetHtmlFile):
        QThread.__init__(self)
        self.targetHtmlFile = targetHtmlFile

    def __del__(self):
        self.wait()

    def run(self):
        """
        main function of the thread
        - initialize shipping info module
        - start main function
        - destroy class
        - destroy thread
        """
        sic = ShippingInfoClass("ShippingInfo.json", self.targetHtmlFile)
        sic.update_ShippingInfo_and_file()
        self.emit(SIGNAL('finished_updating_shipping()'))

class getItemsSoldThread(QThread):
    def __init__(self, days, ids, spreadsheetName):
        QThread.__init__(self)
        self.days = days
        self.ids = ids
        self.spreadsheetName = spreadsheetName

    def __del__(self):
        self.wait()

    def run(self):
        """
        main function of the thread
        - initialize item info module
        - start main function
        - destroy class
        - destroy thread
        """
        iic = ItemInfoClass("ItemInfo.json", self.days, self.ids)
        iic.get_new_items_sold()
        items = sorted(iic.get_items_sorted_by_date().items())

        wb = xlsxwriter.Workbook("output2.xlsx")
        ws = wb.add_worksheet()
        ws.write(3, 0, "Order #")
        ws.write(3, 1, "Date")
        ws.write(3, 2, "Name")
        ws.write(3, 3, "Price of Item")
        ws.write(3, 4, "Cost of Item")
        ws.write(3, 5, "Hassan")
        ws.write(3, 6, "Shipping Cost")
        ws.write(3, 7, "PayPal Fees")
        ws.write(3, 8, "eBay Fees")
        ws.write(3, 9, "Total Cost")
        ws.write(3, 10, "Profit")
        order_num = 1
        row_num = 4
        for item in items:
            transaction_date = item[0]
            item_record = item[1]
            ws.write(row_num, 0, order_num)
            ws.write(row_num, 1, transaction_date)
            ws.write(row_num, 2, item_record['ItemName'])
            ws.write(row_num, 3, item_record['ItemPrice'])
            ws.write(row_num, 4, item_record.get('cost_of_item', 'N/A'))
            ws.write(row_num, 5, "$7.00")
            ws.write(row_num, 6, item_record.get('ShippingLabelCost','N/A'))
            ws.write(row_num, 7, "???")
            ws.write(row_num, 8, "???")
            ws.write(row_num, 9, "???")
            ws.write(row_num, 10, "???")
            order_num = order_num + 1
            row_num = row_num + 1
        wb.close()
        self.emit(SIGNAL('finished_getting_items_sold()'))

def main():
    app = QtGui.QApplication(sys.argv)
    form = eBayApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
