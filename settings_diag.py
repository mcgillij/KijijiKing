# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_diag.ui'
#
# Created: Sun Jul 29 22:28:52 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelSearchTerms = QtGui.QLabel(Dialog)
        self.labelSearchTerms.setObjectName(_fromUtf8("labelSearchTerms"))
        self.gridLayout.addWidget(self.labelSearchTerms, 0, 0, 1, 1)
        self.lineEditSearchTerms = QtGui.QLineEdit(Dialog)
        self.lineEditSearchTerms.setObjectName(_fromUtf8("lineEditSearchTerms"))
        self.gridLayout.addWidget(self.lineEditSearchTerms, 0, 1, 1, 1)
        self.pushAddButton = QtGui.QPushButton(Dialog)
        self.pushAddButton.setDefault(True)
        self.pushAddButton.setObjectName(_fromUtf8("pushAddButton"))
        self.gridLayout.addWidget(self.pushAddButton, 0, 2, 1, 1)
        self.listWidgetSearchTerms = QtGui.QListWidget(Dialog)
        self.listWidgetSearchTerms.setObjectName(_fromUtf8("listWidgetSearchTerms"))
        self.gridLayout.addWidget(self.listWidgetSearchTerms, 1, 0, 1, 3)
        self.labelCity = QtGui.QLabel(Dialog)
        self.labelCity.setObjectName(_fromUtf8("labelCity"))
        self.gridLayout.addWidget(self.labelCity, 2, 0, 1, 1)
        self.lineEditCity = QtGui.QLineEdit(Dialog)
        self.lineEditCity.setObjectName(_fromUtf8("lineEditCity"))
        self.gridLayout.addWidget(self.lineEditCity, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSearchTerms.setText(QtGui.QApplication.translate("Dialog", "Search Terms", None, QtGui.QApplication.UnicodeUTF8))
        self.pushAddButton.setText(QtGui.QApplication.translate("Dialog", "Add Term", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCity.setText(QtGui.QApplication.translate("Dialog", "City: ", None, QtGui.QApplication.UnicodeUTF8))

