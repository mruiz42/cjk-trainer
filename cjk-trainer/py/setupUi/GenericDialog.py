# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GenericDialog.ui',
# licensing of 'GenericDialog.ui' applies.
#
# Created: Wed Apr  3 18:39:02 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_GenericDialog(object):
    def setupUi(self, GenericDialog):
        GenericDialog.setObjectName("GenericDialog")
        GenericDialog.resize(480, 240)
        GenericDialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(GenericDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(GenericDialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(GenericDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GenericDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), GenericDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), GenericDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GenericDialog)

    def retranslateUi(self, GenericDialog):
        GenericDialog.setWindowTitle(QtWidgets.QApplication.translate("GenericDialog", "Generic Dialog", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("GenericDialog", "TextLabel", None, -1))

