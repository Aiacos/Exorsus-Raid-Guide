from bs4 import BeautifulSoup as bs
import requests
import re


class Converter(object):

    def __init__(self, url):
        self.greenColor = '|cFF00FF00xxxxxx|r'
        self.redColor = '|cFFFF0000xxxxxx|r'
        self.grayColor = '|cff808080xxxxxx|r'
        self.spellColor = '|cFF72D5FFxxxxxx|r'
        self.epicColor = '|cFFA335EExxxxxx|r'

        r = requests.get(url)
        soup = bs(r.content, 'html.parser')

        tankSectionTag = soup.find_all('h3', string=re.compile('Summary for Tanks'))[0]
        healerSectionTag = soup.find_all('h3', string=re.compile('Summary for Healers and DPS'))[0]
        dpsSectionTag = soup.find_all('h3', string=re.compile('Summary for Healers and DPS'))[0]

        # ToDo: nomeBoss
        bossName = 'Queen Azshara'

        print(self.finalize(bossName, tankSectionTag, healerSectionTag, dpsSectionTag))

    def extractIconID(self, link):
        id = link.split('/')[-1].split('-')[0]
        return str(id)

    def findTextIcon(self, tag):
        pass

    def wrapTextWith(self, text, wrap):
        s = wrap.replace('xxxxxx', text)
        return s

    def wrapSpell(self, spellID):
        s = '{spell:' + spellID + '}'
        return s

    def contentPrepare(self, contentList):
        contentTextList = []
        # check phase
        if (contentList.name == 'h4'):
            contentTextList.append(self.wrapTextWith(contentList.text, self.grayColor))
            contentList = contentList.next_element.next_element.next_element

        # content
        for li in contentList.children:
            if (li.string):
                contentTextList.append(li.string.rstrip('\n'))
            else:
                text = li.text
                linkTagList = li.find_all('a')
                for linkTag in linkTagList:
                    href = linkTag['href']
                    spellName = linkTag.string
                    text = text.replace(spellName,
                                        self.wrapSpell(self.extractIconID(href)) + self.wrapTextWith(spellName,
                                                                                                     self.spellColor),
                                        1).rstrip('\n')

                contentTextList.append('- ' + text)

        contentText = '\n'.join(contentTextList)
        return contentText.rstrip()

    def contentPrepare3(self, contentList):
        contentTextList = []

        # check phase1
        if (contentList.name == 'h4'):
            contentTextList.append(self.wrapTextWith(contentList.text, self.grayColor))
            contentList = contentList.next_element.next_element.next_element

        print(contentList.prettify())
        lineList = contentList.get_text()  # .find_all(text=True)
        lineList = str(lineList).splitlines()
        for line in lineList:
            # print(line)
            contentTextList.append(line)

        contentText = '\n'.join(contentTextList)
        return contentText.rstrip()

    def finalize(self, bossName, tankSectionTag, healerSectionTag, dpsSectionTag):
        tankContentList = tankSectionTag.next_element.next_element.next_element
        healerContentList = healerSectionTag.next_element.next_element.next_element
        dpsContentList = dpsSectionTag.next_element.next_element.next_element

        # title
        textList = []
        textList.append(self.wrapTextWith(bossName, self.redColor) + '\n')

        # content
        tankText = '{T}' + self.wrapTextWith(tankSectionTag.string, self.greenColor) + '\n' + self.contentPrepare3(
            tankContentList) + '{/T}'
        textList.append(tankText)

        healerText = '{H}' + self.wrapTextWith(healerSectionTag.string, self.greenColor) + '\n' + self.contentPrepare3(
            healerContentList) + '{/H}'
        textList.append(healerText)

        dpsText = '{D}' + self.wrapTextWith(dpsSectionTag.string, self.greenColor) + '\n' + self.contentPrepare3(
            dpsContentList) + '{/D}'
        textList.append(dpsText)

        return ''.join(textList)


if __name__ == '__main__':
    url = 'https://www.icy-veins.com/wow/queen-azshara-strategy-guide-in-the-eternal-palace-raid'
    url2 = 'https://www.icy-veins.com/wow/orgozoa-strategy-guide-in-the-eternal-palace-raid'
    Converter(url)
