from bs4 import BeautifulSoup
import requests
import re
import ftfy

def linkScrape(url, tag, attr, returnList):
    site = requests.get(url)
    soup = BeautifulSoup(site.text, "lxml")
    for link in soup.find_all(tag, attrs=attr):
        topic = re.findall(r'/forums[^"]*', str(link))[0]
        topic = "http://www.jasez.ca" + str(topic)
        returnList.append(topic)

    return returnList

def nextPage(webPage, tag, attr):
    site = requests.get(webPage)
    soup = BeautifulSoup(site.text, "lxml")
    nextPage = soup.find(tag, attrs=attr)
    if nextPage != "http://www.jasez.ca/forums/":
        newWebPage = re.search(r'/forums[^"]*', str(nextPage))[0]
        newWebPage = "http://www.jasez.ca" + str(newWebPage)
        print(newWebPage)
    else:
        newWebPage = None


    return newWebPage

punctuation = "><\n\r"
replace = "    "
transtable = str.maketrans(punctuation, replace)
# Things to do
# monitoring system for thread collection and comment collection
# xml formatting
# conditional parsing so it doesn't take threads that are too short
# figure out what to do about quotations and other repetitive strings
# what sort of cleaning are we going to do

#
# firstSite = {'startLink': 'http://www.jasez.ca/forums',
#              'topics': ['td', {'class': "desc"}],
#              'thread': ['h3', {'class': "topic"}],
#              'next_page': ['div', {'class': "right"}],
#              'name': re.search(r'/profil/[^"]*', str(()))[0],
#              'content': ['td', {'class': 'section'}]}


# directory = []
# startURL = "http://www.jasez.ca/forums"
# linkScrape(startURL, 'td', {'class': "desc"}, directory)
# print(directory)


# count = 0
# for page in directory:
#     fileDump = []
#     while len(page) >= len(directory[count]):
#         linkScrape(page, 'h3', {'class': "topic"}, fileDump)
#         page = nextPage(page, 'div', {'class': "right"})
#         print(page)
#     print(fileDump)
#     with open("jasezlinks3.txt", "a", encoding='utf8') as x:
#         for element in set(fileDump):
#             x.write(element + '\n')
#     count += 1

with open("jasezlinks.txt", 'r', encoding='utf8') as urlDirectory:
    for url in urlDirectory:
        print(url)
        with open('jasezx.xml', 'a', encoding='utf8') as file:
            file.write("<s>")
            while url != "http://www.jasez.ca/forums/" and url is not None:
                site = requests.get(url)
                soup = BeautifulSoup(site.text, "lxml")
                numSpeakers = []
                for post in soup.find_all('tbody', attrs={'class': "post"}):
                    speaker = re.search(r'/profil/[^"]*', str(post()))[0]
                    if speaker not in numSpeakers:
                        numSpeakers.append(speaker)
                    elif len(numSpeakers) >= 2:
                        break
                if len(numSpeakers) >= 2:
                    uidList = []
                    for post in soup.find_all('tbody', attrs={'class': "post"}):
                        speaker = re.search(r'/profil/[^"]*', str(post()))[0]
                        speaker = re.sub(r'/profil/', '', speaker)
                        if speaker in uidList:
                            speaker = uidList.index(speaker) + 1
                        else:
                            uidList.append(speaker)
                            speaker = uidList.index(speaker) + 1
                        rawText = str(post.find('td', attrs={'class': 'section'}))
                        rawText = re.sub(r'.*?</span>', '', rawText)
                        rawText = re.sub(r'<.*?>', '', rawText)
                        rawText = re.sub(r'<|>|\r|\n', '', rawText)
                        rawText = rawText.translate(transtable)
                        cleanText = ftfy.fix_text(rawText)
                        file.write('<utt uid={}>{}</utt>'.format(speaker, cleanText))
                    uidList = []
                url = nextPage(url, 'div', {'class': "right"})
            file.write("</s>\n")