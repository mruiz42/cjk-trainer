# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cjk-trainer/ui/DeckNamePrompt.ui',
# licensing of 'cjk-trainer/ui/DeckNamePrompt.ui' applies.
#
# Created: Tue May 21 11:51:25 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DeckNamePromptDialog(object):
    def setupUi(self, DeckNamePromptDialog):
        DeckNamePromptDialog.setObjectName("DeckNamePromptDialog")
        DeckNamePromptDialog.resize(480, 176)
        DeckNamePromptDialog.setSizeGripEnabled(False)
        DeckNamePromptDialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(DeckNamePromptDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_selectStudyLanguages = QtWidgets.QLabel(DeckNamePromptDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_selectStudyLanguages.sizePolicy().hasHeightForWidth())
        self.label_selectStudyLanguages.setSizePolicy(sizePolicy)
        self.label_selectStudyLanguages.setObjectName("label_selectStudyLanguages")
        self.verticalLayout_2.addWidget(self.label_selectStudyLanguages)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_vocabulary = QtWidgets.QLabel(DeckNamePromptDialog)
        self.label_vocabulary.setObjectName("label_vocabulary")
        self.verticalLayout_5.addWidget(self.label_vocabulary)
        self.comboBox_vocabulary = QtWidgets.QComboBox(DeckNamePromptDialog)
        self.comboBox_vocabulary.setObjectName("comboBox_vocabulary")
        self.verticalLayout_5.addWidget(self.comboBox_vocabulary)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_definition = QtWidgets.QLabel(DeckNamePromptDialog)
        self.label_definition.setObjectName("label_definition")
        self.verticalLayout_3.addWidget(self.label_definition)
        self.comboBox_definition = QtWidgets.QComboBox(DeckNamePromptDialog)
        self.comboBox_definition.setCurrentText("")
        self.comboBox_definition.setObjectName("comboBox_definition")
        self.verticalLayout_3.addWidget(self.comboBox_definition)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.lineEdit_enterDeckName = QtWidgets.QLineEdit(DeckNamePromptDialog)
        self.lineEdit_enterDeckName.setObjectName("lineEdit_enterDeckName")
        self.verticalLayout_2.addWidget(self.lineEdit_enterDeckName)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(DeckNamePromptDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DeckNamePromptDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DeckNamePromptDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DeckNamePromptDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DeckNamePromptDialog)

    def retranslateUi(self, DeckNamePromptDialog):
        DeckNamePromptDialog.setWindowTitle(QtWidgets.QApplication.translate("DeckNamePromptDialog", "Create a new deck", None, -1))
        self.label_selectStudyLanguages.setText(QtWidgets.QApplication.translate("DeckNamePromptDialog", "Select study languages", None, -1))
        self.label_vocabulary.setToolTip(QtWidgets.QApplication.translate("DeckNamePromptDialog", "Language for the vocabulary words being learned.", None, -1))
        self.label_vocabulary.setText(QtWidgets.QApplication.translate("DeckNamePromptDialog", "Vocabulary", None, -1))
        self.label_definition.setToolTip(QtWidgets.QApplication.translate("DeckNamePromptDialog", "Language for the definition of the vocabulary word which the user can easily understand.", None, -1))
        self.label_definition.setText(QtWidgets.QApplication.translate("DeckNamePromptDialog", "Definition", None, -1))
        self.lineEdit_enterDeckName.setPlaceholderText(QtWidgets.QApplication.translate("DeckNamePromptDialog", "Enter new deck name here...", None, -1))

