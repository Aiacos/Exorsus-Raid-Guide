from bs4 import BeautifulSoup as bs
import requests
import re


class ExpansionParser():
    pass

class RaidParser():
    pass

class BossParser():

    def __init__(self, url):

        r = requests.get(url)
        soup = bs(r.content, 'html.parser')

        self.raidDict = self.parseBossList(soup)
        # for keys, values in self.raidDict.items():
        #     print(keys)
        #     if keys == 'mainPage':
        #         print values[0], values[1]
        #     else:
        #         for i in values:
        #             print i[0], i[1]

    def parseBossList(self, soup):
        raidDict = {}
        raidBossList = soup.find_all('div', class_='toc_page_list_items')[0]
        raidPage = raidBossList.find_all('span')[0]
        bossTagList = raidBossList.contents[3:-2:2]

        bossList = []
        for boss in bossTagList:
            bossList.append([boss.a.find_all('span')[1].get_text(), boss.a['href'].replace('//', '')])

        # dict structure mainPage <- [Name, url]
        # dict structure bossList <- [, [Name, url]]
        raidDict['mainPage'] = [raidPage.a.find_all('span')[1].get_text(), raidPage.a['href'].replace('//', '')]
        raidDict['bossList'] = bossList

        return raidDict

    def getRaidBossDict(self):
        return self.raidDict

    def getBossList(self):
        return self.raidDict['bossList']

    def getMainPage(self):
        return self.raidDict['mainPage']

class TactParser(object):

    def __init__(self, url):

        r = requests.get(url)
        soup = bs(r.content, 'html.parser')

        # boss Name
        self.bossName = soup.find('span', class_='toc_page_list_item selected').get_text().replace('\n', ' ').strip()

        # sezioni
        tankSectionTag = soup.find_all('h3', string=re.compile('Summary for Tanks'))[0]
        healerSectionTag = soup.find_all('h3', string=re.compile('Summary for Healers and DPS'))[0]
        dpsSectionTag = soup.find_all('h3', string=re.compile('Summary for Healers and DPS'))[0]

        # contentuto delle sezioni
        self.tankDict = self.checkSection(tankSectionTag)
        self.healerDict = self.checkSection(healerSectionTag)
        self.dpsDict = self.checkSection(dpsSectionTag)


    def checkSection(self, section):
        contentTextList = []
        contentTextDict = {}

        # print section
        contentTextDict['section'] = section


        # title Phase: 2.8.1. Phase One
        titlePhaseList = []
        sectionID = section['id'] + '-\d'
        for p in section.find_next_siblings('h4', id=re.compile(sectionID)):
            # print p
            # print type(p)
            # print '-------------'
            titlePhaseList.append(p)

        if len(titlePhaseList) > 0:
            phaseList = []
            for t in titlePhaseList:
                # print 'TITLE: ', t.text
                # print 'TITLE CONTENT: ', t.find_next_sibling('ul')
                phaseList.append(self.parseList(t))

            contentTextDict['h4PhaseList'] = phaseList
            contentTextDict['ContentList'] = []
        else:
            contentList = self.parseList(section)
            contentTextDict['h4PhaseList'] = []
            contentTextDict['ContentList'] = contentList

        return contentTextDict #contentTextList    #.rstrip().replace('\n\n', '\n')

    def getBossTactTagDict(self):
        bossDict = {}

        bossDict['boss'] = self.bossName
        bossDict['tank'] = self.tankDict
        bossDict['healer'] = self.healerDict
        bossDict['dps'] = self.dpsDict

        return bossDict


    def parseList(self, section):
        liList = []

        # list Phase: During Phase One
        for i in section.find_next_sibling('ul'):
            if i.string != '\n':
                # print 'TAG: ', i.name
                # print 'CONENUTO: ', i.contents # [phase, inner li]

                # Phase
                if i.contents[0].name == 'b' and i.contents[1].name == 'ul':
                    # print 'SECTION: no Phase'

                    liList.append(i.contents[0])
                    liList.append(i.contents[1])

                # no Phase
                else:
                    # print 'SECTION: Phase'
                    # print 'FIX LIST:', bs(str(i), 'html.parser')
                    liList.append(bs(str(i), 'html.parser'))


                # print 'TIPO: ', type(i)
                # print '-------------'

        return liList


    def _testNextElement(self, sectionTag):
        # tag.nam: restituisce il nome del tag
        print sectionTag, type(sectionTag)
        print '-----------------START----------------'
        print sectionTag.next_element, type(sectionTag.next_element)
        print '--------------------------------------'
        print sectionTag.next_element.next_element.next_element, type(sectionTag.next_element.next_element.next_element)
        print '----------------DEBUG---------------'
        test = sectionTag.next_element.next_element.next_element
        print 'tag', test.name
        print 'string: ', test.string
        print 'text: ', test.text
        print '----------------- END -----------------'





if __name__ == '__main__':
    url = 'https://www.icy-veins.com/wow/queen-azshara-strategy-guide-in-the-eternal-palace-raid'
    url2 = 'https://www.icy-veins.com/wow/orgozoa-strategy-guide-in-the-eternal-palace-raid'
    url3 = 'https://www.icy-veins.com/wow/za-qul-harbinger-of-ny-alotha-strategy-guide-in-the-eternal-palace-raid'

    c = TactParser(url)
    #print c.tankDict['section']
    #print c.tankDict['h4PhaseList']
    #print c.tankDict['ContentList']
    #print c.get_text()