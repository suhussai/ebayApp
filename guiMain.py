import time
import serial
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, SIGNAL
import sys
import design
import os
import json
from ItemInfoModule import ItemInfoClass
from ShippingInfoModule import ShippingInfoClass
from ItemsHeldModule import ItemsHeldClass

class eBayApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(eBayApp, self).__init__(parent)
        self.setupUi(self)
        self.ser = None
        self.users = None
        self.currentUser = None
        self.currentUserCredentials = None
        self.users_file = "users.json"
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
        self.btns = [self.btnUpdateShipping, self.btnGetItemsSold, self.btnSelectAsCurrentUser, self.btnDeleteUser, self.btnAddUser]
        #print(self.spinBoxDays.value())

    def addNewItem(self):
        """
        add new item with:
        - long name from self.lineLongName.text()
        - short name from self.lineShortName.text()
        - cost of item from self.spinCostOfItem.value()
        Note: quick process, separate thread not required
        """
        ihc = ItemsHeldClass("ItemsHeld.json")
        long_name = str(self.lineLongName.text())
        short_name = str(self.lineShortName.text())
        cost_of_item = str(self.doubleSpinCostOfItem.value())
        ihc.add_entry(long_name, short_name, cost_of_item)

    def updateShipping(self):
        """
        - prepare thread and start
        the thread for the
        update shipping process
        """
        self.setAllButtons(self.btnGetItemsSold, False)
        #days, ids = get_credentials_of_selected_user()
        self.targetHtmlFile = "target.html"
        self.get_thread = updateShippingInfoThread(self.targetHtmlFile)
        self.connect(self.get_thread, SIGNAL('finished_updating_shipping()'), self.finished_getting_items_sold)
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

        self.get_thread = getItemsSoldThread(days, ids)
        self.connect(self.get_thread, SIGNAL('update_items_sold_tree(QString, QString)'), self.update_items_sold_tree)
        self.connect(self.get_thread, SIGNAL('finished_getting_items_sold()'), self.finished_getting_items_sold)

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

    def update_items_sold_tree(self, item, itemInfo):
        print("adding these items")
        print(item, itemInfo)
        QtGui.QTreeWidgetItem(self.treeWidgetItemsSold.invisibleRootItem(), [item, itemInfo])
        #item.setData(0, QtCore.Qt.UserRole, item)
        #self.treeWidgetItemsSold.setData(0, QtGui.QTreeWidgetItem(item))

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
    def __init__(self, days, ids):
        QThread.__init__(self)
        self.days = days
        self.ids = ids

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
        for item, itemInfo in iic.requestedItemsSold.iteritems():
            itemName = itemInfo['ItemName']
            time.sleep(0.5)
            self.emit(SIGNAL('update_items_sold_tree(QString,QString)'), str(itemName), str(itemInfo))

        self.emit(SIGNAL('finished_getting_items_sold()'))

def main():
    app = QtGui.QApplication(sys.argv)
    form = eBayApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
