import time
import serial
from PyQt4 import QtGui
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
        #print(self.spinBoxDays.value())

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
        
        
    def setupSerial(self):
        # https://pyserial.readthedocs.org/en/latest/shortintro.html
        self.ser = serial.Serial()
        self.ser.baudrate = int(self.baudRate.text())
        self.ser.port = str(self.portName.text())
        self.ser.open()

        self.get_thread = getSerialMessages(self.ser, self.Values_To_Montior)
        self.connect(self.get_thread, SIGNAL('updateValue(QString, QString)'), self.updateValue)

        self.get_thread.start()
        print("thread started")
        #self.btnShutdown.clicked.connect(self.get_thread.terminate)

    def teardownSerial(self):
        self.get_thread.terminate()
        self.ser.close()
        print("thread terminated")

    def updateValue(self, ID, value):
        print("Updating value")
        print("ID " + str(ID) + " Value " + str(value))
        if (self.Values_To_Montior.get(str(ID), None) is not None): 
            self.Values_To_Montior[str(ID)] = value 
            self.displayValues()

    def displayValues(self):
        print("displaying!!!")
        self.fieldDisplay.clear()
        for ID, value  in self.Values_To_Montior.iteritems():
            formatted_string = str(ID) + " : " + str(value)
            print("adding item " + formatted_string)
            self.fieldDisplay.addItem(formatted_string)

    def setupFileHandler(fileName):
        #http://www.tutorialspoint.com/python/python_files_io.htm
        fileHandler = open(fileName, "w+")
        # FCTEMP2:-1, TANKPRES:-1, FCTEMP1:-1, AMTEMP2:-1, AMTEMP1:-1, ERROR:-1, FCPRES:-1, FCVOLT:-1, FCCURR:-1, CAPCURR:-1
        fileHandler.write("Time, FCTEMP2, TANKPRES, FCTEMP1, AMTEMP2, AMTEMP1, ERROR, FCPRES, FCVOLT, FCCURR, CAPCURR\n")
        return fileHandler

    def teardownFileHandler(fileHandler):
        fileHandler.close()

    def writeToLog(fileHandler, Values_To_Montior):
        #http://www.tutorialspoint.com/python/python_date_time.htm
        message = str(time.asctime(time.localtime(time.time()))) + " "
        for ID, value in Values_To_Montior.iteritems():
            message +=  "%d, " % (int(value))
            
        message += "\n"
        fileHandler.write(message)

class getSerialMessages(QThread):    
    def __init__(self, ser, Values_To_Montior):
        QThread.__init__(self)
        self.Values_To_Montior = Values_To_Montior
        self.ser = ser

    def __del__(self):
        self.wait()            
        
        
    def run(self):
        while True:
            line = self.ser.readline() # read line
            print("from thread...")
            print("line is " + line)
            if len(line) > 0:
                try:
                    (ID, value) = line.split() # get id and value
                    self.emit(SIGNAL('updateValue(QString,QString)'), ID, value)
                except:
                    pass

    


def main():
    app = QtGui.QApplication(sys.argv)
    form = eBayApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

    
#### Arduino Code
#### http://electronics.stackexchange.com/questions/87868/data-lost-writing-on-arduino-serial-port-overflow
# void setup(){
#   Serial.begin(9600);
# }
# void loop(){
#   Serial.println("FCTEMP2 20");   
#   Serial.flush();
#   delay(1000);
# }


