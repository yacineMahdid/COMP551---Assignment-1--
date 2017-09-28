import scrapy
import zipfile
import os
import shutil
import datetime
import shutil
import io

class QuotesSpider(scrapy.Spider):
    name = "theater"
    start_urls = [
        #'https://fr.wikisource.org/wiki/Les_Chevaliers_(trad._Eug%C3%A8ne_Talbot)',
        #'https://fr.wikisource.org/wiki/L%E2%80%99%C3%82ge_d%E2%80%99or'
        'https://fr.wikisource.org/wiki/Cat%C3%A9gorie:Com%C3%A9dies'
    ]
    conversationsLocation = '/home/2013/mbouch95/cp551/p1/tutorial/tutorial/conversationsTheater'
    conversationFileName = 'theater.xml'
    isClean = False

    def parse(self, response):

        #clean folders 
        if not self.isClean:
            shutil.rmtree(self.conversationsLocation) 
            os.makedirs(self.conversationsLocation)
            os.mknod(self.conversationsLocation + '/' + self.conversationFileName)
            self.isClean = True 

        for a in response.css('div.mw-category-group > ul > li > a::attr(href)'):
            link = response.urljoin(a.extract())
            yield scrapy.Request(link, callback=self.parseTheaterPiece)
   
    def parseTheaterPiece(self, response): 
        characterToId = dict() 
        characters = []
        characterIdCounter = 1
        dialogues = []    

        #get title of piece
        title = response.css('#firstHeading::text').extract_first()
        title = u'%s' % title

        #here's a list of characters by responses
        #print('characters list ' + str(len(response.css('span.personnage::text'))))
        #print('dialogue list ' + str(len(response.css('div + p::text'))))
       
        #TODO
        #mayn paragraphs may follow a character. adjsut css accrodingly
        #italics in charcter names can make weird behaviour
       
        theaterText = response.css('div + p::text')
        if len(theaterText) == 1:
            theaterText = response.css('div.Texte > p::text')

            for line in theaterText:

                #convert to unicode
                line = u'%s' % line.extract()

                # split on big unicode hypen to seperate text from 
                splitLine = line.split(u'\u2014')

                #get character from the split string
                character = splitLine.pop(0).strip()

                #if no split, then it is not a line
                if len(splitLine) == 0:
                    continue

                #add character to dictionary if possible
                if character not in characterToId:
                    characterToId[character] = characterIdCounter
                    characterIdCounter = characterIdCounter + 1

                characters.append(character)

                dialogue = u''.join(splitLine)
                dialogues.append(dialogue)

        else:
            #section for div + p
            characterss = response.css('span.personnage::text')

            for character in characterss:
                character = character.extract()
                if character not in characterToId:
                    characterToId[character] = characterIdCounter
                    characterIdCounter = characterIdCounter + 1

                characters.append(character)

            for line in theaterText:
                dialogues.append(line.extract())

        zippedList = zip(characters, dialogues)

        path = self.conversationsLocation + '/' + self.conversationFileName
        with io.open(path, "a", encoding='utf8') as f:
            f.write(u'<dialog>\n')
            f.write(u'\t<s>\n')

            for character, dialogue in zippedList:
                characterId = characterToId[character]

                #write to file
                t = u'\t\t<utt uid=\"%d\"> %s </utt>\n' %(characterId, dialogue)
                f.write(t)

            #write footer for file
            f.write(u'\t</s>\n')
            f.write(u'</dialog>\n')   