from bs4 import BeautifulSoup
import requests
import re
import ftfy
from urllib import request


def linkScrape(url, tag, attr, returnList):
    site = requests.get(url)
    soup = BeautifulSoup(site.text, "lxml")
    for link in soup.find_all(tag, attrs=attr):
        topic = re.findall(r'/forums[^"]*', str(link))[0]
        topic = "http://www.smail.fr" + str(topic)
        returnList.append(topic)

    return returnList

def nextPage(webPage, tag, attr):
    sock = request.urlopen(webPage)
    site = sock.read()
    soup = BeautifulSoup(site, "lxml")
    nextPage = soup.find(tag, attrs=attr)
    if nextPage != None:
        newWebPage = re.search(r'/forums[^"]*', str(nextPage))[0]
        newWebPage = "http://www.smail.fr" + str(newWebPage)
        print(newWebPage)

        return newWebPage


# thirdSite = {'startLink': "http://www.smail.fr/forums/",
#              'topics': ['div', {'class': "content"}],
#              'thread': ['td', {'class': "topic"}],
#              'next_page': ['a', {'class': "icon ui item"}],
#              'name': re.search(r'data-username=[^"]*', str(()))[0],
#              'content': ['td', {'class': 'section'}]}


directory = []
startURL = "http://www.smail.fr/forums/"
linkScrape(startURL, 'div', {'class': "content"}, directory)
print(directory)

for page in directory:
    fileDump = []
    while page is not None:
        linkScrape(page, 'td', {'class': "topic"}, fileDump)
        page = nextPage(page, 'div', {'class': 'right small menu'})
        print(page)
    print(fileDump)
    with open("smallfrlinks2.txt", "a", encoding='utf8') as x:
        for element in set(fileDump):
            x.write(element + '\n')


with open("smallfrlinks.txt", 'r', encoding='utf8') as urlDirectory:
    for url in urlDirectory:
        print(url)
        with open('smailfr.xml', 'a', encoding='utf8') as file:
            file.write("<s>")
            while url is not None:
                try:
                    # the requset library returned a 410 error despite the existance of the page
                    #this solution still occasionally returned such an error, necessitating the error handling
                    sock = request.urlopen(url)
                    site = sock.read()
                    soup = BeautifulSoup(site, "lxml")
                    numSpeakers = []
                    for link in soup.find_all('td', attrs={'class': "message"}):
                        speaker = re.search(r'/profil/[^"]*', str(link()))
                        if speaker not in numSpeakers:
                            numSpeakers.append(speaker)
                        elif len(numSpeakers) >= 2:
                            break
                    if len(numSpeakers) >= 2:
                        uidList = []
                        for post in soup.find_all('td', attrs={'class': "message"}):
                            speaker = re.search(r'/profil/[^"]*', str(post))[0]
                            speaker = re.sub(r'/profil/', '', speaker)
                            if speaker in uidList:
                                speaker = uidList.index(speaker) + 1
                            else:
                                uidList.append(speaker)
                                speaker = uidList.index(speaker) + 1
                            rawText = str(post.find('p', attrs={'itemprop': 'text'}))
                            rawText = re.sub(r'.*?</span>', '', rawText)
                            rawText = re.sub(r'<.*?>', '', rawText)
                            rawText = re.sub(r'<|>|\n|\r', '', rawText)
                            cleanText = ftfy.fix_text(rawText)
                            file.write('<utt uid={}>{}</utt>'.format(speaker, cleanText))
                        uidList = []
                except:
                    print("HTTPERROR")
                    break
                url = nextPage(url, 'a', {'class': "icon ui item"})
            file.write("</s>\n")
