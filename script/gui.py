#!usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

from PySide2.QtCore import QObject, QThread, Signal
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QTextEdit, QMessageBox
from PySide2.QtWidgets import QLineEdit, QPushButton, QProgressBar, QVBoxLayout, QLabel

from main import Converter


class RaidGuideGui(QMainWindow):
    """
    The class generates the graphical interface of the application. This cannot be changed.
    There are two input fields for the url list and for deciding the destination folder.
    """
    WIDTH = 640  # define width of windows
    HEIGHT = 480  # define height of windows

    def __init__(self):
        """
        GUI constructor, the structure that will appear on the screen is specified.
        """
        super(RaidGuideGui, self).__init__()
        # initialize the main windows set constant dimension and title
        self.resize(self.WIDTH, self.HEIGHT)
        # TODO dare un titolo alla finestra
        self.setWindowTitle("Titolo provvisorio")
        self.setMaximumSize(self.WIDTH, self.HEIGHT)
        self.setMinimumSize(self.WIDTH, self.HEIGHT)

        # line edit form for url
        self.url_line_edit = QLineEdit(self)
        self.url_line_edit.setGeometry(15, 80, 610, 20)
        self.url_line_edit.setPlaceholderText(
            "https://www.icy-veins.com/wow/queen-azshara-strategy-guide-in-the-eternal-palace-raid")
        # TODO modificare la funzione lambda con una funzione migliore di controllo
        self.url_line_edit.textChanged[str].connect(
            lambda: self.run_btn.setEnabled(self.url_line_edit.text() != ""))

        # line edit form for save file in specific folder
        # TODO deve essere completato
        self.outfile_line_edit = QLineEdit(self)
        self.outfile_line_edit.setGeometry(15, 130, 497, 20)
        self.outfile_line_edit.setPlaceholderText(
            "https://www.icy-veins.com/wow/queen-azshara-strategy-guide-in-the-eternal-palace-raid")

        # button execute
        self.run_btn = QPushButton(self)
        self.run_btn.setGeometry(512, 226, 113, 32)
        self.run_btn.setText("Run")
        self.run_btn.setDisabled(True)
        self.run_btn.clicked.connect(self.start_conversion)

        # button save
        self.save_btn = QPushButton(self)
        self.save_btn.setGeometry(512, 266, 113, 32)
        self.save_btn.setText("Save")
        self.save_btn.setDisabled(True)
        self.save_btn.clicked.connect(self.export_on_file)

        # button exit
        self.exit_btn = QPushButton(self)
        self.exit_btn.setGeometry(512, 306, 113, 32)
        self.exit_btn.setText("Exit")
        self.exit_btn.clicked.connect(app.exit)

        # button file dialog
        self.file_dialog = QPushButton(self)
        self.file_dialog.setGeometry(512, 126, 113, 32)
        self.file_dialog.setText("browse")

        # create text area
        self.text_area = QTextEdit(self)
        self.text_area.setGeometry(15, 160, 497, 305)
        self.text_area.setReadOnly(True)

        # launch gui
        self.show()

    def start_conversion(self):
        url = self.url_line_edit.text()
        pb = ProgressBar(self)
        pb.process_link(url)

    def export_on_file(self):
        ret = QMessageBox.warning(self, self.tr("My Application"),
                                  self.tr("The document has been modified.\n" +
                                          "Do you want to save your changes?"),
                                  QMessageBox.Save | QMessageBox.Discard
                                  | QMessageBox.Cancel,
                                  QMessageBox.Save)
        if ret == QMessageBox.Save:
            print("click saved")
            # Save was clicked
        elif ret == QMessageBox.Discard:
            # Don't save was clicked
            print("click don't saved")
        elif ret == QMessageBox.Cancel:
            print("click Cancel")
        # cancel was clicked


class ProgressBar(QDialog):
    WIDTH = 640  # define width of windows
    HEIGHT = 150  # define height of windows

    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent)
        # initialize the main windows set constant dimension and title
        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("Progress...")
        self.setMaximumSize(self.WIDTH, self.HEIGHT)
        self.setMinimumSize(self.WIDTH, self.HEIGHT)
        layout = QVBoxLayout(self)

        # Create a label for work in progress
        self.work_in_progress = QLabel(self)
        self.work_in_progress.setText("Please be patient...")
        layout.addWidget(self.work_in_progress)

        # Create a progress bar the main layout
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 1)
        layout.addWidget(self.progress_bar)

        # init task
        self.myLongTask = TaskThread()
        self.myLongTask.taskFinished.connect(self.onFinished)

        # open dialog
        self.show()

    def process_link(self, url):
        """
        Start the conversion process from the html page, run the process in a separate thread.
        :param url: [str] the address of the page to be analyzed is required
        """

        self.myLongTask.setUrl(url)
        self.onStart()

    def onStart(self):
        self.progress_bar.setRange(0, 0)
        self.myLongTask.start()

    def onFinished(self):
        # Stop the pulsation
        self.progress_bar.setRange(0, 1)
        time.sleep(0.5)
        self.close()


class TaskThread(QThread):
    taskFinished = Signal()
    url = None

    def __init__(self):
        super(TaskThread, self).__init__()
        pass

    def setUrl(self, url):
        self.url = url

    def run(self):
        Converter(self.url)
        self.taskFinished.emit()

class StreamText(QObject):
        newText = Signal(str)

        def write(self, text):
            self.newText.emit(str(text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    frame = RaidGuideGui()
    frame.show()
    sys.exit(app.exec_())
