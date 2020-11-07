from py.StarDelegate import *
from PySide2.QtCore import *
from PySide2 import QtGui
from PySide2.QtGui import QColor
from py.driverUi.callMainWindow import MainWindow
# ADDED KEYPRESS EATER TAB BAR
# self.tabBar = QtWidgets.QTabBar()
# self.tabWidget.setTabBar(self.tabBar)

DB_PATH = './data/vocab2.db'


def setDarkStyleSheet(qApp:QApplication):
    qApp.setStyle(QStyleFactory.create("Fusion"))
    darkPalette = QtGui.QPalette()
    darkPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    darkPalette.setColor(QtGui.QPalette.WindowText, Qt.white)
    darkPalette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    darkPalette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    darkPalette.setColor(QtGui.QPalette.ToolTipBase, Qt.white)
    darkPalette.setColor(QtGui.QPalette.ToolTipText, Qt.white)
    darkPalette.setColor(QtGui.QPalette.Text, Qt.white)
    darkPalette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    darkPalette.setColor(QtGui.QPalette.ButtonText, Qt.white)
    darkPalette.setColor(QtGui.QPalette.BrightText, Qt.red)
    darkPalette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    darkPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    darkPalette.setColor(QtGui.QPalette.HighlightedText, Qt.black)
    qApp.setPalette(darkPalette)
    qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setDarkStyleSheet(app)
    # view = QQuickView()
    # url = QUrl("../ui/view.qml")
    # view.setSource(url)
    # view.show()
    win = MainWindow(DB_PATH)
    #win.show()
    #win.loadDeckList()
    # view = QQuickView()
    # container = Q Widget.createWindowContainer(view, win)
    # view.setSource(QUrl("../ui/view.qml"))
    # view.setClearBeforeRendering(True)
    # container.setMinimumHeight(430)
    # container.setMinimumWidth(800)
    # container.setAutoFillBackground(True)
    clear = QColor(67,67,0)
    clear.setAlpha(0)
    # view.setColor(clear)
    geom = QRect(60, 80, 880, 880)
    win.ui.horizontalLayout_2.setGeometry(geom)
    # win.ui.horizontalLayout_2.addWidget(container, alignment=Qt.AlignCenter)
    # print(view.Ready)
    # print(view.errors())
    # view.raise_()
    # view.show()


    #win.reloadTableList()
    # win.nameOfCurrentTable = win.ui.deckList.item(0).data(0)
    # print(win.nameOfCurrentTable)
    # win.loadWordTable(0)



    #win.database.closeDatabase()
    sys.exit(app.exec_())
