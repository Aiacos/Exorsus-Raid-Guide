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
        tankContentList = tankSectionTag.next_element.next_element.next_element
        healerContentList = healerSectionTag.next_element.next_element.next_element
        dpsContentList = dpsSectionTag.next_element.next_element.next_element

        #print dpsContentList :: <h4 id="sec-2-8-1">2.8.1. Phase One</h4>

        #self.checkSection2(tankSectionTag)
        self.checkSection2(dpsSectionTag)


    def checkSection(self, section):
        sectionContentList = section.next_element.next_element.next_element
        if sectionContentList.name == 'ul':
            # only one list
            for li in sectionContentList.findChildren():
                print li
                print type(li)
                print '-------------'
                for ul in li:
                    # print ul
                    # print type(ul)
                    # print '-------------'
                    pass


        if sectionContentList.name == 'h4':
            print section
            phaseList = section.find_all('h4')
            print phaseList
            #print phaseList.contents
            #for p in phaseList:
                #print p

    def checkSection2(self, section):
        contentTextList = []

        print section

        # title Phase: 2.8.1. Phase One
        titlePhaseList = []
        sectionID = section['id'] + '-\d'
        for p in section.find_next_siblings('h4', id=re.compile(sectionID)):
            #print p
            #print type(p)
            #print '-------------'
            titlePhaseList.append(p)

        # list Phase: During Phase One
        for i in section.find_next_sibling('ul'):
            if i.string != '\n':
                print 'TAG: ', i.name
                print 'CONENUTO: ', i.contents
                print 'TIPO: ', type(i)
                print '-------------'

        return contentTextList#.rstrip().replace('\n\n', '\n')



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