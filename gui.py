#!usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QFileDialog
from PySide2.QtCore import Slot


class RaidGuideGui(QMainWindow):
    """
    The class generates the graphical interface of the application. This cannot be changed.
    There are two input fields for the url list and for deciding the destination folder.
    """
    WIDTH = 640  # define width of windows
    HEIGHT = 325  # define height of windows

    def __init__(self):
        """
        GUI constructor, the structure that will appear on the screen is specified.
        """
        super(RaidGuideGui, self).__init__()
        # initialize the main windows set constant dimension and title
        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("Titolo provvisorio")  # TODO dare un titolo alla finestra
        self.setMaximumSize(self.WIDTH, self.HEIGHT)
        self.setMinimumSize(self.WIDTH, self.HEIGHT)

        # line edit form for url
        self.url_line_edit = QLineEdit(self)
        self.url_line_edit.setGeometry(15, 80, 610, 20)
        self.url_line_edit.setPlaceholderText(
            "https://www.icy-veins.com/wow/queen-azshara-strategy-guide-in-the-eternal-palace-raid")

        # line edit form for url
        self.outfile_line_edit = QLineEdit(self)
        self.outfile_line_edit.setGeometry(15, 130, 497, 20)
        self.outfile_line_edit.setPlaceholderText(
            "https://www.icy-veins.com/wow/queen-azshara-strategy-guide-in-the-eternal-palace-raid")

        # button execute
        self.run_btn = QPushButton(self)
        self.run_btn.setGeometry(512, 226, 113, 32)
        self.run_btn.setText("Run")
        self.run_btn.setDisabled(True)

        # button exit
        self.exit_btn = QPushButton(self)
        self.exit_btn.setGeometry(512, 266, 113, 32)
        self.exit_btn.setText("Exit")


        # button file dialog
        self.file_dialog = QPushButton(self)
        self.file_dialog.setGeometry(512, 126, 113, 32)
        self.file_dialog.setText("browse")

        self.show()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    frame = RaidGuideGui()
    sys.exit(app.exec_())
