# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImportCsvDialog.ui',
# licensing of 'ImportCsvDialog.ui' applies.
#
# Created: Fri Apr  5 08:25:34 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ImportCsvDialog(object):
    def setupUi(self, ImportCsvDialog):
        ImportCsvDialog.setObjectName("ImportCsvDialog")
        ImportCsvDialog.resize(800, 480)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../ico/appicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ImportCsvDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(ImportCsvDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_separator = QtWidgets.QLabel(ImportCsvDialog)
        self.label_separator.setObjectName("label_separator")
        self.verticalLayout_2.addWidget(self.label_separator)
        self.comboBox_separator = QtWidgets.QComboBox(ImportCsvDialog)
        self.comboBox_separator.setFrame(True)
        self.comboBox_separator.setObjectName("comboBox_separator")
        self.comboBox_separator.addItem("")
        self.comboBox_separator.addItem("")
        self.comboBox_separator.addItem("")
        self.comboBox_separator.addItem("")
        self.comboBox_separator.addItem("")
        self.verticalLayout_2.addWidget(self.comboBox_separator)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.lineEdit_tableName = QtWidgets.QLineEdit(ImportCsvDialog)
        self.lineEdit_tableName.setAcceptDrops(False)
        self.lineEdit_tableName.setObjectName("lineEdit_tableName")
        self.verticalLayout.addWidget(self.lineEdit_tableName)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(ImportCsvDialog)
        self.plainTextEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_numLines = QtWidgets.QLabel(ImportCsvDialog)
        self.label_numLines.setText("")
        self.label_numLines.setObjectName("label_numLines")
        self.horizontalLayout_4.addWidget(self.label_numLines)
        self.buttonBox = QtWidgets.QDialogButtonBox(ImportCsvDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_4.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(ImportCsvDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ImportCsvDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ImportCsvDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ImportCsvDialog)

    def retranslateUi(self, ImportCsvDialog):
        ImportCsvDialog.setWindowTitle(QtWidgets.QApplication.translate("ImportCsvDialog", "Import from CSV", None, -1))
        self.label_separator.setText(QtWidgets.QApplication.translate("ImportCsvDialog", "Separator", None, -1))
        self.comboBox_separator.setItemText(0, QtWidgets.QApplication.translate("ImportCsvDialog", ",", None, -1))
        self.comboBox_separator.setItemText(1, QtWidgets.QApplication.translate("ImportCsvDialog", "tab", None, -1))
        self.comboBox_separator.setItemText(2, QtWidgets.QApplication.translate("ImportCsvDialog", ";", None, -1))
        self.comboBox_separator.setItemText(3, QtWidgets.QApplication.translate("ImportCsvDialog", "-", None, -1))
        self.comboBox_separator.setItemText(4, QtWidgets.QApplication.translate("ImportCsvDialog", "/", None, -1))
        self.lineEdit_tableName.setPlaceholderText(QtWidgets.QApplication.translate("ImportCsvDialog", "Name of new deck", None, -1))
        self.plainTextEdit.setPlaceholderText(QtWidgets.QApplication.translate("ImportCsvDialog", "Vocabulary,Definition,Pronunciation(optional)", None, -1))

