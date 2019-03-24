# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/importDeck.ui',
# licensing of './ui/importDeck.ui' applies.
#
# Created: Sun Mar 24 01:32:22 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_importDialog(object):
    def setupUi(self, importDialog):
        importDialog.setObjectName("importDialog")
        importDialog.resize(831, 575)
        self.verticalLayout = QtWidgets.QVBoxLayout(importDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(importDialog)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(importDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(importDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(importDialog)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), importDialog.accept)

        QtCore.QObject.connect(self.buttonBox, self.accepted, importDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), importDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(importDialog)

    def retranslateUi(self, importDialog):
        importDialog.setWindowTitle(QtWidgets.QApplication.translate("importDialog", "Create a new deck", None, -1))
        self.plainTextEdit.setPlainText(QtWidgets.QApplication.translate("importDialog", "<VOCABULARY><ROMANIZATION><DEFINITION>\n", None, -1))
        self.plainTextEdit.setPlaceholderText(QtWidgets.QApplication.translate("importDialog", "Enter some words", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("importDialog", "NULL", None, -1))


    def donothing(self):
        print("donothing")
    def accepted(self):
        returned = self.plainTextEdit.copy()
        print(returned)