from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, SIGNAL
import genericDialog

class genDialog(QtGui.QDialog, genericDialog.Ui_Dialog):
    def __init__(self, textToDisplay="Not Set", parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.labelOutput.setText(textToDisplay)
        self.btnConfirm.clicked.connect(self.closeDialog)
        self.setProgressValue(0)

    def setText(self, newText):
        self.labelOutput.setText(newText)

    def closeDialog(self):
        self.done(0)

    def setProgressValue(self, newValue):
        """
        assigns 'newValue' to be the
        new the progress bar value
        """
        try:
            self.progressBar.setValue(int(newValue))
            if (int(newValue) >= 100):
                self.labelOutput.setText("Finished!")
        except:
            self.progressBar.setValue(0)
    def getProgressValue(self):
        return self.progressBar.value()

    def disableProgressBar(self):
        self.progressBar.hide()

    def enableOKButton(self):
        self.btnConfirm.setEnabled(True)

    def disableOKButton(self):
        self.btnConfirm.setEnabled(False)

    def formatForGenericErrorDisplaying(self):
        self.enableOKButton()
        self.disableProgressBar()

    def formatForGenericActionNotFinished(self):
        self.disableOKButton()
        self.disableProgressBar()
        self.show()
    def formatForGenericActionFinished(self):
        self.setText("Finished!")
        self.enableOKButton()
        self.disableProgressBar()
