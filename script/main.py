from bs4 import BeautifulSoup as bs
import requests
from Parser import TactParser
from Converter import Converter


if __name__ == '__main__':
    url = 'https://www.icy-veins.com/wow/queen-azshara-strategy-guide-in-the-eternal-palace-raid'
    url2 = 'https://www.icy-veins.com/wow/orgozoa-strategy-guide-in-the-eternal-palace-raid'
    url3 = 'https://www.icy-veins.com/wow/za-qul-harbinger-of-ny-alotha-strategy-guide-in-the-eternal-palace-raid'

    p = TactParser(url2)
    c = Converter(p.getBossTactTagDict())
    print c.get_text()


