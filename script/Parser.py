from bs4 import BeautifulSoup as bs
import requests
import re

class Converter(object):

    def __init__(self, url):

        r = requests.get(url)
        soup = bs(r.content, 'html.parser')

        # sezioni
        tankSectionTag = soup.find_all('h3', string=re.compile('Summary for Tanks'))[0]
        healerSectionTag = soup.find_all('h3', string=re.compile('Summary for Healers and DPS'))[0]
        dpsSectionTag = soup.find_all('h3', string=re.compile('Summary for Healers and DPS'))[0]

        # contentuto delle sezioni
        self.checkSection(tankSectionTag)
        self.checkSection(healerSectionTag)
        self.checkSection(dpsSectionTag)


    def checkSection(self, section):
        contentTextList = []
        contentTextDict = {}

        print section
        contentTextDict['section'] = section


        # title Phase: 2.8.1. Phase One
        titlePhaseList = []
        sectionID = section['id'] + '-\d'
        for p in section.find_next_siblings('h4', id=re.compile(sectionID)):
            print p
            print type(p)
            print '-------------'
            titlePhaseList.append(p)

        if len(titlePhaseList) > 0:
            phaseList = []
            for t in titlePhaseList:
                print 'TITLE: ', t.text
                print 'TITLE CONTENT: ', t.find_next_sibling('ul')
                phaseList.append(self.parseList(t))

            contentTextDict['PhaseList'] = phaseList
            contentTextDict['ContentList'] = []
        else:
            contentList = self.parseList(section)
            contentTextDict['PhaseList'] = []
            contentTextDict['ContentList'] = contentList

        return contentTextDict #contentTextList    #.rstrip().replace('\n\n', '\n')


    def parseList(self, section):
        liList = []

        # list Phase: During Phase One
        for i in section.find_next_sibling('ul'):
            if i.string != '\n':
                print 'TAG: ', i.name
                print 'CONENUTO: ', i.contents # [phase, inner li]

                # Phase
                if i.contents[0].name == 'b' and i.contents[1].name == 'ul':
                    print 'SECTION: no Phase'

                    liList.append(i.contents[0])
                    liList.append(i.contents[1])

                # no Phase
                else:
                    print 'SECTION: Phase'
                    print 'FIX LIST:', bs(str(i), 'html.parser')


                print 'TIPO: ', type(i)
                print '-------------'

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

    c = Converter(url)
    #print c.get_text()