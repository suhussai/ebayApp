# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created: Sun Jan 24 12:45:42 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(623, 748)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.listUsers = QtGui.QListWidget(self.tab)
        self.listUsers.setObjectName(_fromUtf8("listUsers"))
        self.verticalLayout.addWidget(self.listUsers)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.btnSelectAsCurrentUser = QtGui.QPushButton(self.tab)
        self.btnSelectAsCurrentUser.setObjectName(_fromUtf8("btnSelectAsCurrentUser"))
        self.verticalLayout.addWidget(self.btnSelectAsCurrentUser)
        self.btnDeleteUser = QtGui.QPushButton(self.tab)
        self.btnDeleteUser.setObjectName(_fromUtf8("btnDeleteUser"))
        self.verticalLayout.addWidget(self.btnDeleteUser)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        self.label_8 = QtGui.QLabel(self.tab)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout.addWidget(self.label_8)
        self.lineUserName = QtGui.QLineEdit(self.tab)
        self.lineUserName.setObjectName(_fromUtf8("lineUserName"))
        self.verticalLayout.addWidget(self.lineUserName)
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.lineAppID = QtGui.QLineEdit(self.tab)
        self.lineAppID.setObjectName(_fromUtf8("lineAppID"))
        self.verticalLayout.addWidget(self.lineAppID)
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.lineCertID = QtGui.QLineEdit(self.tab)
        self.lineCertID.setObjectName(_fromUtf8("lineCertID"))
        self.verticalLayout.addWidget(self.lineCertID)
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout.addWidget(self.label_6)
        self.lineDevID = QtGui.QLineEdit(self.tab)
        self.lineDevID.setObjectName(_fromUtf8("lineDevID"))
        self.verticalLayout.addWidget(self.lineDevID)
        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout.addWidget(self.label_7)
        self.lineTokenID = QtGui.QLineEdit(self.tab)
        self.lineTokenID.setObjectName(_fromUtf8("lineTokenID"))
        self.verticalLayout.addWidget(self.lineTokenID)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        self.btnAddUser = QtGui.QPushButton(self.tab)
        self.btnAddUser.setObjectName(_fromUtf8("btnAddUser"))
        self.verticalLayout.addWidget(self.btnAddUser)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.label_2 = QtGui.QLabel(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_4.addWidget(self.label_2)
        self.spinBoxDays = QtGui.QSpinBox(self.tab_2)
        self.spinBoxDays.setMinimum(1)
        self.spinBoxDays.setMaximum(60)
        self.spinBoxDays.setObjectName(_fromUtf8("spinBoxDays"))
        self.verticalLayout_4.addWidget(self.spinBoxDays)
        self.btnGetItemsSold = QtGui.QPushButton(self.tab_2)
        self.btnGetItemsSold.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGetItemsSold.sizePolicy().hasHeightForWidth())
        self.btnGetItemsSold.setSizePolicy(sizePolicy)
        self.btnGetItemsSold.setObjectName(_fromUtf8("btnGetItemsSold"))
        self.verticalLayout_4.addWidget(self.btnGetItemsSold)
        self.btnRefreshRecords = QtGui.QPushButton(self.tab_2)
        self.btnRefreshRecords.setObjectName(_fromUtf8("btnRefreshRecords"))
        self.verticalLayout_4.addWidget(self.btnRefreshRecords)
        self.btnUpdateShipping = QtGui.QPushButton(self.tab_2)
        self.btnUpdateShipping.setObjectName(_fromUtf8("btnUpdateShipping"))
        self.verticalLayout_4.addWidget(self.btnUpdateShipping)
        self.btnExportToSpreadsheet = QtGui.QPushButton(self.tab_2)
        self.btnExportToSpreadsheet.setObjectName(_fromUtf8("btnExportToSpreadsheet"))
        self.verticalLayout_4.addWidget(self.btnExportToSpreadsheet)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem4)
        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_4.addWidget(self.label_3)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem5)
        self.treeItemsHeld = QtGui.QTreeWidget(self.tab_2)
        self.treeItemsHeld.setObjectName(_fromUtf8("treeItemsHeld"))
        self.verticalLayout_4.addWidget(self.treeItemsHeld)
        self.label_11 = QtGui.QLabel(self.tab_2)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.verticalLayout_4.addWidget(self.label_11)
        self.lineLongName = QtGui.QLineEdit(self.tab_2)
        self.lineLongName.setObjectName(_fromUtf8("lineLongName"))
        self.verticalLayout_4.addWidget(self.lineLongName)
        self.label_10 = QtGui.QLabel(self.tab_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_4.addWidget(self.label_10)
        self.lineShortName = QtGui.QLineEdit(self.tab_2)
        self.lineShortName.setObjectName(_fromUtf8("lineShortName"))
        self.verticalLayout_4.addWidget(self.lineShortName)
        self.label_9 = QtGui.QLabel(self.tab_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_4.addWidget(self.label_9)
        self.doubleSpinCostOfItem = QtGui.QDoubleSpinBox(self.tab_2)
        self.doubleSpinCostOfItem.setObjectName(_fromUtf8("doubleSpinCostOfItem"))
        self.verticalLayout_4.addWidget(self.doubleSpinCostOfItem)
        self.btnAddNewItem = QtGui.QPushButton(self.tab_2)
        self.btnAddNewItem.setObjectName(_fromUtf8("btnAddNewItem"))
        self.verticalLayout_4.addWidget(self.btnAddNewItem)
        self.btnDeleteItem = QtGui.QPushButton(self.tab_2)
        self.btnDeleteItem.setObjectName(_fromUtf8("btnDeleteItem"))
        self.verticalLayout_4.addWidget(self.btnDeleteItem)
        self.btnUpdateItemsHeldFromFile = QtGui.QPushButton(self.tab_2)
        self.btnUpdateItemsHeldFromFile.setObjectName(_fromUtf8("btnUpdateItemsHeldFromFile"))
        self.verticalLayout_4.addWidget(self.btnUpdateItemsHeldFromFile)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 623, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QtGui.QToolBar(MainWindow)
        self.toolBar_2.setObjectName(_fromUtf8("toolBar_2"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Users", None))
        self.btnSelectAsCurrentUser.setText(_translate("MainWindow", "Select As Current User", None))
        self.btnDeleteUser.setText(_translate("MainWindow", "Delete User", None))
        self.label_8.setText(_translate("MainWindow", "User Name", None))
        self.label_4.setText(_translate("MainWindow", "AppID", None))
        self.label_5.setText(_translate("MainWindow", "CertID", None))
        self.label_6.setText(_translate("MainWindow", "DevID", None))
        self.label_7.setText(_translate("MainWindow", "TokenID", None))
        self.btnAddUser.setText(_translate("MainWindow", "Add User", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "User Management", None))
        self.label_2.setText(_translate("MainWindow", "Days", None))
        self.btnGetItemsSold.setText(_translate("MainWindow", "Get Items Sold", None))
        self.btnRefreshRecords.setText(_translate("MainWindow", "Refresh Records", None))
        self.btnUpdateShipping.setText(_translate("MainWindow", "Update Shipping", None))
        self.btnExportToSpreadsheet.setText(_translate("MainWindow", "Export to Spreadsheet", None))
        self.label_3.setText(_translate("MainWindow", "Items Held", None))
        self.treeItemsHeld.headerItem().setText(0, _translate("MainWindow", "Long Name", None))
        self.treeItemsHeld.headerItem().setText(1, _translate("MainWindow", "Short Name", None))
        self.treeItemsHeld.headerItem().setText(2, _translate("MainWindow", "Cost of Item", None))
        self.label_11.setText(_translate("MainWindow", "Long Name", None))
        self.label_10.setText(_translate("MainWindow", "Short Name", None))
        self.label_9.setText(_translate("MainWindow", "Cost of Item", None))
        self.btnAddNewItem.setText(_translate("MainWindow", "Add New Item", None))
        self.btnDeleteItem.setText(_translate("MainWindow", "Delete Item", None))
        self.btnUpdateItemsHeldFromFile.setText(_translate("MainWindow", "Update Items Held From File", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Item Management", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2", None))

