from bs4 import BeautifulSoup as bs
import requests
from Parser import TactParser, BossParser
from Converter import Converter


if __name__ == '__main__':
    url1 = 'https://www.icy-veins.com/wow/abyssal-commander-sivara-strategy-guide-in-the-eternal-palace-raid'
    url = 'https://www.icy-veins.com/wow/the-queens-court-strategy-guide-in-the-eternal-palace-raid'
    url2 = 'https://www.icy-veins.com/wow/za-qul-harbinger-of-ny-alotha-strategy-guide-in-the-eternal-palace-raid'
    url3 = 'https://www.icy-veins.com/wow/queen-azshara-strategy-guide-in-the-eternal-palace-raid'

    b = BossParser(url)
    boss = b.getBossList()[0][1]
    print boss

    p = TactParser(boss)
    c = Converter(p.getBossTactTagDict())
    print c.get_text()


