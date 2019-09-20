from bs4 import BeautifulSoup as bs


class Converter(object):

    def __init__(self, bossDict):
        self.greenColor = '|cFF00FF00xxxxxx|r'
        self.redColor = '|cFFFF0000xxxxxx|r'
        self.grayColor = '|cff808080xxxxxx|r'
        self.spellColor = '|cFF72D5FFxxxxxx|r'
        self.epicColor = '|cFFA335EExxxxxx|r'

        self.text = self.convert(bossDict['boss'], bossDict['tank'], bossDict['healer'], bossDict['dps'])

    def extractIconID(self, link):
        id = link.split('/')[-1].split('-')[0]
        return str(id)

    def replaceSpells(self, text, spellDict):
        for name, id in spellDict.items():
            spell = self.wrapSpell(id) + self.wrapTextWith(name, self.spellColor)
            text = text.replace(name, spell)

        return text

    def findSpells(self, tag):
        spellDict = {}

        spellList = tag.find_all('a')
        if spellList:
            for spell in spellList:
                id = self.extractIconID(spell['href'])
                spellName = spell.text
                spellDict[spellName] = id

        return spellDict

    def wrapTextWith(self, text, wrap):
        s = wrap.replace('xxxxxx', text)
        return s

    def wrapSpell(self, spellID):
        s = '{spell:' + spellID + '}'
        return s

    def prepareSummaryTitle(self, l):
        newList = [l[0], l[1:]]
        return newList

    def contentPrepareFromBS(self, contentTextDict):
        # section
        section = contentTextDict['section'].get_text()

        # content
        content = []
        if contentTextDict['h4PhaseList']:
            for line, counter in zip(contentTextDict['h4PhaseList'], range(len(contentTextDict['h4PhaseList']))):
                if counter % 2:
                    for li in line:
                        # for li in i:
                        spellDict = self.findSpells(li)
                        text = str(li.text).replace('\n', ' ').replace('  ', ' ').strip()
                        text = self.replaceSpells(text, spellDict)
                        content.append('- ' + text)
                else:
                    content.append(self.wrapTextWith(str(line.text), self.grayColor))
        elif contentTextDict['ContentList']:
            for li in contentTextDict['ContentList']:
                spellDict = self.findSpells(li)
                text = str(li.text).replace('\n', ' ').replace('  ', ' ').strip()
                text = self.replaceSpells(text, spellDict)
                content.append('- ' + text)

        else:
            content = ''

        return section, '\n'.join(content)

    def convert(self, bossName, tankContentList, healerContentList, dpsContentList):
        tankContentList = self.contentPrepareFromBS(tankContentList)
        healerContentList = self.contentPrepareFromBS(healerContentList)
        dpsContentList = self.contentPrepareFromBS(dpsContentList)

        # title
        textList = []
        textList.append(self.wrapTextWith(bossName, self.redColor) + '\n')

        # content
        tankText = '{T}' + self.wrapTextWith(tankContentList[0], self.greenColor) + '\n' + tankContentList[1] + '{/T}'
        textList.append(tankText)

        healerText = '{H}' + self.wrapTextWith(healerContentList[0],
                                               self.greenColor) + '\n' + healerContentList[1] + '{/H}'
        textList.append(healerText)

        dpsText = '{D}' + self.wrapTextWith(dpsContentList[0], self.greenColor) + '\n' + dpsContentList[1] + '{/D}'
        textList.append(dpsText)

        return ''.join(textList)

    def get_text(self):
        return self.text


if __name__ == '__main__':
    tankString = """
    2.7. Summary for Tanks
    Make sure to be closest to the other tank on the pull and at the start of Phases Two and Four, so that Mind Tether links the two tanks.
    Make sure to be within 12 yards of each other whenever possible to keep the Mind Tether damage as low as possible.
    Do not tank the boss directly in the center of the room (since this is where the Crushing Grasp tentacle will often hit).
    Pick up the Horrific Vision adds and bring them in melee range so the DPS can cleave them.
    During Phases Two and Three, pull the boss into the Maddening Eruption Icon Maddening Eruption void zones to soak them and ensure that the boss is debuffed by them.
    During Phase Four, face the boss towards the inside of the room so that the Caustic Delirium Icon Caustic Delirium void zones do not spawn in the Dark Beyond Icon Dark Beyond.
    """

    healerString = """
    2.8. Summary for Healers and DPS
    2.8.1. Phase One
    Avoid entering the Dark Beyond Icon Dark Beyond around the outer edges of the room.
    Avoid getting hit by the Crushing Grasp Icon Crushing Grasp tentacle.
    Dispel players affected by Dread Icon Dread in a staggered way, and heal up the raid-wide damage.
    Do not stand in the Portal of Madness Icon Portal of Madness void zones.
    Focus the Horrific Summoners and cleave down the Horrific Visions.
    2.8.2. Phases Two and Three
    Avoid entering the Dark Beyond Icon Dark Beyond around the outer edges of the room.
    Avoid getting hit by the Crushing Grasp Icon Crushing Grasp tentacle.
    Dispel players affected by Dread Icon Dread in a staggered way, and heal up the raid-wide damage.
    Heal the increasing raid-wide damage from Hysteria Icon Hysteria.
    Move away from allies affected by Manifest Nightmares Icon Manifest Nightmares. If affected by Manifest Nightmares, drop the resulting void zones in the center of the room, either overlapping them or leaving gaps between them.
    Do not stand in the Maddening Eruption Icon Maddening Eruption void zone.
    During Phase Three, assigned DPS players enter the Delirium Realm Icon Delirium Realm by standing in Delirium's Descent Icon Delirium's Descent void zones.
    During Phase Three, healers must make sure to heal up and dispel players who exit the Delirium Realm Icon Delirium Realm.
    2.8.3. Phase Four
    Avoid entering the Dark Beyond Icon Dark Beyond around the outer edges of the room.
    Avoid getting hit by the Crushing Grasp Icon Crushing Grasp tentacle.
    Dispel players affected by Manic Dread Icon Manic Dread in a staggered way, and heal up the raid-wide damage.
    Assigned DPS players enter the Delirium Realm Icon Delirium Realm by standing in Caustic Delirium Icon Caustic Delirium void zones in order to break the boss's damage absorption shield and interrupt Dark Pulse Icon Dark Pulse.
    Assigned healers and DPS players use the Fear's Gate Icon Fear's Gate portals to enter the Fear Realm and focus the Horrific Summoners.
    """

    dpsString = healerString

    # testDict = {"boss": "Queen Azshara", "tank": tankString.splitlines(), "healer": healerString.splitlines(), "dps": dpsString.splitlines()}

    ########################################

    # c = Converter(testDict)
    # print c.get_text()
