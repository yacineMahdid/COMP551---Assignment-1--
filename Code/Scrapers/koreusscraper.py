from bs4 import BeautifulSoup
import requests
import re
import ftfy

def linkScrape(url, tag, attr, returnList):
    site = requests.get(url)
    soup = BeautifulSoup(site.text, "lxml")
    for link in soup.find_all(tag, attrs=attr):
        topic = re.findall(r'http[^"]*', str(link))
        if len(topic) > 0:
            returnList.append(topic[0])

    return returnList

def linkScrape1(url, tag, attr, returnList):
    site = requests.get(url)
    soup = BeautifulSoup(site.text, "lxml")
    for link in soup.find_all(tag, attrs=attr):
        topic = re.findall(r'topic[^"]*', str(link))[0]
        topic = "https://www.koreus.com/modules/newbb/" + str(topic)
        if len(topic) > 0:
            returnList.append(topic)

    return returnList

def nextPage(webPage, tag, attr):
    site = requests.get(webPage)
    soup = BeautifulSoup(site.text, "lxml")
    nextPage = soup.find(tag, attrs=attr)
    if re.search('>.*?<', str(nextPage)) != None:
        # koreus loops at the end of the thread, as the last page button disappears and instead the last href link is to the previous page
        newWebPage = re.findall(r'/topic.*?<', str(nextPage))[-1]
        # the solution was to get a bit more of the link, which on the last page, and only the last page, ends in a number
        newPage = newWebPage.split('"')[0]
        EOF = newWebPage.split('"')[1]
        # if the number is present, break the loop and move on to the next thread
        if any(char.isdigit() for char in EOF):
            newWebPage = None
            return newWebPage
        newWebPage = "https://www.koreus.com/modules/newbb" + newPage
        print(newWebPage)

        return newWebPage



startURL = "https://www.koreus.com/modules/newbb/"
linkScrape(startURL, 'span', {'class': "item"}, directory)

directory = ['https://www.koreus.com/modules/newbb/forum8-96000.html']

for page in directory:
    fileDump = []
    history = []
    count = 0
    # koreus loops when the end of thread is reached between the last and second last page
    # by referencing visited pages, a break condition is (hackily) created
    # a better solution can be found in the updated nextpage function which was not used for this first part of the scrape
    while page is not None:
        history.append(page)
        linkScrape1(page, 'tr', {'class': "even" or "odd"}, fileDump)
        page = nextPage(page, 'div', {'style': "float: right; text-align:right;"})
        print(page)
        if len(history) != len(set(history)):
            break
        count += 1
        if count >= 200:
            print(fileDump)
            with open("koreuslinks.txt", "a", encoding='utf8') as x:
                for element in set(fileDump):
                    x.write(element + '\n')
            count = 0
            fileDump = []
            history = []
    print(fileDump)
    with open("koreuslinks.txt", "a", encoding='utf8') as x:
        for element in set(fileDump):
            x.write(element + '\n')


punctuation = "><\n\r"
replace = "    "
transtable = str.maketrans(punctuation, replace)

with open("koreuslinks.txt", 'r', encoding='utf8') as urlDirectory:
    for url in urlDirectory:
        print(url)
        with open('koreus.xml', 'a', encoding='utf8') as file:
            file.write("<s>")
            while url != "https://www.koreus.com/modules/newbb/" and url is not None:
                try:
                    site = requests.get(url)
                    soup = BeautifulSoup(site.text, "lxml")
                    numSpeakers = []
                    for post in soup.find_all('table', attrs={'class': "outer"}):
                        speaker = re.search(r'href="/membre/[^"]*', str(post))[0]
                        # This prevents scraping of links with 2 or fewer users
                        if speaker not in numSpeakers:
                            numSpeakers.append(speaker)
                        elif len(numSpeakers) >= 3:
                            break
                    if len(numSpeakers) >= 3:
                        uidList = []
                        # Sets the uid so that anyone new gets added, and anyone responding again gets the same ID as before
                        for post in soup.find_all('table', attrs={'class': "outer"}):
                            speaker = re.search(r'href="/membre/[^"]*', str(post()))[0]
                            speaker = re.sub(r'href="/membre/', '', speaker)
                            if speaker in uidList:
                                speaker = uidList.index(speaker) + 1
                            else:
                                uidList.append(speaker)
                                speaker = uidList.index(speaker) + 1
                            rawText = str(post.find('div', attrs={'class': 'comText'}))
                            rawText = re.sub(r'.*?</blockquote>', '', rawText)
                            rawText = re.sub(r'<.*?>', '', rawText)
                            rawText = re.sub(r'<|>|\r|\n', '', rawText)
                            rawText = rawText.translate(transtable)
                            # ftfy is a library that stands for fix text for you, and it eliminates most encoding errors that occur
                            cleanText = ftfy.fix_text(rawText)
                            file.write('<utt uid={}>{}</utt>'.format(speaker, cleanText))
                        uidList = []
                except:
                    print("HTTPERROR")
                    break
                url = nextPage(url, 'div', {'style': "float: right; text-align:right;"})
            file.write("</s>\n")
