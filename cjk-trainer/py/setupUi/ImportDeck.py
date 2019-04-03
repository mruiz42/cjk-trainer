# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/importDeck.ui',
# licensing of './ui/importDeck.ui' applies.
#
# Created: Sun Mar 24 05:17:21 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
from py.utilities.SQLTools import *
from py.utilities.CSVTools import importDialogHelper

class Ui_importDialog(object):
    def setupUi(self, importDialog):
        importDialog.setObjectName("importDialog")
        importDialog.resize(831, 575)
        self.verticalLayout = QtWidgets.QVBoxLayout(importDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(importDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(importDialog)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_Import = QtWidgets.QPushButton(importDialog)
        self.pushButton_Import.setObjectName("pushButton_Import")
        self.horizontalLayout.addWidget(self.pushButton_Import)
        self.pushButton_Cancel = QtWidgets.QPushButton(importDialog)
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.horizontalLayout.addWidget(self.pushButton_Cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(importDialog)
        QtCore.QMetaObject.connectSlotsByName(importDialog)

    def retranslateUi(self, importDialog):
        importDialog.setWindowTitle(QtWidgets.QApplication.translate("importDialog", "Create a new deck", None, -1))
        self.lineEdit.setPlaceholderText(
            QtWidgets.QApplication.translate("importDialog", "New Flashcard Deck", None, -1))
        self.plainTextEdit.setPlainText(
            QtWidgets.QApplication.translate("importDialog", "<VOCABULARY><PRONUNCIATION><DEFINITION>\n"
                                                             "", None, -1))
        self.plainTextEdit.setPlaceholderText(
            QtWidgets.QApplication.translate("importDialog", "Default Format = <VOCABULARY><ROMANIZATION><DEFINITION> ",
                                             None, -1))
        self.pushButton_Import.setText(QtWidgets.QApplication.translate("importDialog", "Import", None, -1))
        self.pushButton_Cancel.setText(QtWidgets.QApplication.translate("importDialog", "Cancel", None, -1))
