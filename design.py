# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created: Wed Jan  6 19:55:21 2016
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
        MainWindow.resize(783, 619)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.listUsers = QtGui.QListWidget(self.centralwidget)
        self.listUsers.setObjectName(_fromUtf8("listUsers"))
        self.verticalLayout.addWidget(self.listUsers)
        self.btnSelectAsCurrentUser = QtGui.QPushButton(self.centralwidget)
        self.btnSelectAsCurrentUser.setObjectName(_fromUtf8("btnSelectAsCurrentUser"))
        self.verticalLayout.addWidget(self.btnSelectAsCurrentUser)
        self.btnDeleteUser = QtGui.QPushButton(self.centralwidget)
        self.btnDeleteUser.setObjectName(_fromUtf8("btnDeleteUser"))
        self.verticalLayout.addWidget(self.btnDeleteUser)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout.addWidget(self.label_8)
        self.lineUserName = QtGui.QLineEdit(self.centralwidget)
        self.lineUserName.setObjectName(_fromUtf8("lineUserName"))
        self.verticalLayout.addWidget(self.lineUserName)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.lineAppID = QtGui.QLineEdit(self.centralwidget)
        self.lineAppID.setObjectName(_fromUtf8("lineAppID"))
        self.verticalLayout.addWidget(self.lineAppID)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.lineCertID = QtGui.QLineEdit(self.centralwidget)
        self.lineCertID.setObjectName(_fromUtf8("lineCertID"))
        self.verticalLayout.addWidget(self.lineCertID)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout.addWidget(self.label_6)
        self.lineDevID = QtGui.QLineEdit(self.centralwidget)
        self.lineDevID.setObjectName(_fromUtf8("lineDevID"))
        self.verticalLayout.addWidget(self.lineDevID)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout.addWidget(self.label_7)
        self.lineTokenID = QtGui.QLineEdit(self.centralwidget)
        self.lineTokenID.setObjectName(_fromUtf8("lineTokenID"))
        self.verticalLayout.addWidget(self.lineTokenID)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.btnAddUser = QtGui.QPushButton(self.centralwidget)
        self.btnAddUser.setObjectName(_fromUtf8("btnAddUser"))
        self.verticalLayout.addWidget(self.btnAddUser)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_4.addWidget(self.label_3)
        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.verticalLayout_4.addWidget(self.treeWidget)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_4.addWidget(self.label_2)
        self.spinBoxDays = QtGui.QSpinBox(self.centralwidget)
        self.spinBoxDays.setMinimum(1)
        self.spinBoxDays.setMaximum(60)
        self.spinBoxDays.setObjectName(_fromUtf8("spinBoxDays"))
        self.verticalLayout_4.addWidget(self.spinBoxDays)
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.verticalLayout_4.addWidget(self.pushButton_4)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.verticalLayout_4.addWidget(self.pushButton_2)
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.verticalLayout_4.addWidget(self.pushButton_3)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 783, 25))
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
        self.label_3.setText(_translate("MainWindow", "Items Sold", None))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "ItemName", None))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "DateSold", None))
        self.label_2.setText(_translate("MainWindow", "Days", None))
        self.pushButton_4.setText(_translate("MainWindow", "Get Items Sold", None))
        self.pushButton_2.setText(_translate("MainWindow", "Update Shipping", None))
        self.pushButton_3.setText(_translate("MainWindow", "Update Items Held", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2", None))

