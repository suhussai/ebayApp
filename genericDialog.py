# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'genericDialog.ui'
#
# Created: Sun Jan 10 12:10:52 2016
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(323, 119)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelOutput = QtGui.QLabel(Dialog)
        self.labelOutput.setObjectName(_fromUtf8("labelOutput"))
        self.verticalLayout.addWidget(self.labelOutput)
        self.btnConfirm = QtGui.QPushButton(Dialog)
        self.btnConfirm.setObjectName(_fromUtf8("btnConfirm"))
        self.verticalLayout.addWidget(self.btnConfirm)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.labelOutput.setText(_translate("Dialog", "Change for occasion", None))
        self.btnConfirm.setText(_translate("Dialog", "Ok", None))

