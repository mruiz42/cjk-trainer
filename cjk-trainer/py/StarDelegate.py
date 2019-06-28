from PySide2.QtWidgets import *
from PySide2 import QtCore
from utilities.SqlTools import *
class StarDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def paint(self, painter, option, index):
        # TODO Bug where enabling delegate creation will use high amount of cpu indefinitely
        #  Possible infinite loop

        chk_bx = self.parent.indexWidget(index)
        if not chk_bx:
            chk_bx = QCheckBox()
            chk_bx.setStyleSheet("QCheckBox::indicator { width: 32px; height: 32px}"
                                 "QCheckBox::indicator:checked{image: url(../ico/starred.png)}"
                                 "QCheckBox::indicator:unchecked{image: url(../ico/unstarred.png)}")

            chk_bx.setGeometry(option.rect)
            self.parent.setIndexWidget(index, chk_bx)
            chk_bx.clicked.connect(lambda: self.onClick(index, self.parent.model()))

            if index.data() == 0:
                chk_bx.setCheckState(QtCore.Qt.CheckState.Unchecked)
            elif index.data() == 1:
                chk_bx.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            return

    def onClick(self,index, model):
        switchedVal = -1
        if index.data() == 0:
            switchedVal = 1
        elif index.data() == 1:
            switchedVal = 0
        model.setData(index, switchedVal)

        # chk_bx.stateChanged.connect(self.mainWindow.updateStarredValue)
        # lay_out = QHBoxLayout(chk_bx)
        # lay_out.addWidget(chk_bx)
        # lay_out.setAlignment(QtCore.Qt.AlignCenter)
        # lay_out.setContentsMargins(0,0,0,0)
        # chk_bx.stateChanged.connect()

'''         # print("Creating ⭐ cell widget")
            chk_bx = QCheckBox()
            chk_bx.setStyleSheet("QCheckBox::indicator { width: 32px; height: 32px}"
                                 "QCheckBox::indicator:checked{image: url(../ico/starred.png)}"
                                 "QCheckBox::indicator:unchecked{image: url(../ico/unstarred.png)}")
            if checked == 0:
                chk_bx.setCheckState(QtCore.Qt.CheckState.Unchecked)
            elif checked == 1:
                chk_bx.setCheckState(QtCore.Qt.CheckState.Checked)
            # lay_out = QHBoxLayout(chk_bx)
            # lay_out.addWidget(chk_bx)
            # lay_out.setAlignment(QtCore.Qt.AlignCenter)
            # lay_out.setContentsMargins(0,0,0,0)
            chk_bx.stateChanged.connect(self.updateStarredValue)
            return chk_bx
'''