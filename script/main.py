# -*- coding: utf-8 -*-
#!usr/local/bin/ python

import sys
from bs4 import BeautifulSoup as bs
import requests
from PySide2 import QtWidgets

from parser import TactParser
from converter import Converter
from gui import RaidGuideMainWindow


def test():
    """Test function."""
    url = 'https://www.icy-veins.com/wow/the-queens-court-strategy-guide-in-the-eternal-palace-raid'
    url2 = 'https://www.icy-veins.com/wow/za-qul-harbinger-of-ny-alotha-strategy-guide-in-the-eternal-palace-raid'
    url3 = 'https://www.icy-veins.com/wow/queen-azshara-strategy-guide-in-the-eternal-palace-raid'

    p = TactParser(url)
    c = Converter(p.getBossTactTagDict())
    print(c.get_text())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    frame = RaidGuideMainWindow()
    frame.show()
    sys.exit(app.exec_())
