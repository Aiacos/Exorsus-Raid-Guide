#!usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PySide2 import QtWidgets

from parser import TactParser, BossParser
from converter import Converter


class RaidGuideMainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(RaidGuideMainWindow, self).__init__(parent)
        self.form_widget = RaidGuideGui(self)
        self.setCentralWidget(self.form_widget)

        # menu bar
        self.menuBar = self.menuBar()
        self.menuBar.addMenu('File')

        # status bar
        self.statusBar = self.statusBar()
        self.progressBar = QtWidgets.QProgressBar()
        self.statusBar.addWidget(self.progressBar)


class RaidGuideGui(QtWidgets.QWidget):
    """
    The class generates the graphical interface of the application. This cannot be changed.
    There are two input fields for the url list and for deciding the destination folder.
    """
    WIDTH = 640  # define width of windows
    HEIGHT = 480  # define height of windows

    def __init__(self, parent=None):
        """
        GUI constructor, the structure that will appear on the screen is specified.
        """
        super(RaidGuideGui, self).__init__(parent)

        # initialize Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # title
        self.setWindowTitle('Guide Parser')

        # url
        self.urlLineEdit = QtWidgets.QLineEdit()
        self.urlLineEdit.setPlaceholderText(
            'https://www.icy-veins.com/wow/the-eternal-palace-raid-guides-for-battle-for-azeroth')
        self.layout.addWidget(self.urlLineEdit)

        # boss ComboBox
        self.bossList = BossParser(self.urlLineEdit.placeholderText())
        self.bossComboBox = QtWidgets.QComboBox()
        for boss in self.bossList.getBossList().keys():
            self.bossComboBox.addItem(boss)
        self.layout.addWidget(self.bossComboBox)

        # inner layout
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.buttonLayout)
        # output Area
        self.outTextArea = QtWidgets.QPlainTextEdit()
        self.buttonLayout.addWidget(self.outTextArea)

        # self.buttonLayout.addWidget(self.reloadButton)
        # self.buttonLayout.addWidget(self.updateButton)

        # connect
        self.bossComboBox.activated.connect(self.updateTextArea)

        # launch gui
        self.show()

        self.updateTextArea()

    def updateTextArea(self):
        # emit start

        selectedBoss = self.bossComboBox.currentText()
        #print selectedBoss
        parser = TactParser(self.bossList.getBossList()[selectedBoss])
        convert = Converter(parser.getBossTactTagDict())
        self.outTextArea.setPlainText(convert.get_text())

        # emit end


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    frame = RaidGuideMainWindow()
    frame.show()
    sys.exit(app.exec_())
