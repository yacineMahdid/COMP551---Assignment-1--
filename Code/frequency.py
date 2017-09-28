import re

setList = []


standardWords = ['de', 'la', 'le', 'et', 'en', "l'", 'les', 'des', 'est', 'du', "d'", 'un', 'il', 'une', 'dans', 'par', 'au', 'pour', 'qui', 'a', 'que', 'sur', 'son', 'avec', 'plus', 'se', 'l', 'sont', 'ou', 'ce', 'elle', 'sa', 'd', "s'", 'aux', 'comme', 'ses', "qu'", 'été', 'cette', 'pas', 'mais', 'ne', 'deux', 'on', 'fut', 'après', 'entre', 'était', 'fait', 'ont', 'même', "n'", 'lui', 'sous', 'être', 'leur', 'aussi', 'y', 'où', 'dont', 'ainsi', 'ces', 'alors', "c'", 'autres', 'ville', 'ils', 'France', 'nom', 'peut', 'saint', 'également', 'premier', 'très', 'depuis', 'ans', 'années', 'première', 'partie', 'tout', 's', 'lors', 'puis', 'plusieurs', 'groupe', 'français', 'né', 'contre', 'avant', 'bien', 'trois', 'nord', 'guerre', 'commune', 'grand', 'histoire', 'sud', 'avait', 'pays']




def frequencycount(inputFile):
    with open(inputFile, "r", encoding='utf8') as x:
        for element in x:
            setList.append(element)
    nonstandard = "«»¤¡♥°ºœ¨ùø§¹"
    replace = "             "
    transtable = str.maketrans(nonstandard, replace)
    count = 0
    freq = {}
    for element in setList:
        element = element.lower()
        element = re.sub(r'<.*?>', '', element)
        element = re.sub(r'https?:\/\/.*?[ \n]', '', element)
        element = re.sub(r'www.*?[ \n]', '', element)
        newElement = []
        # Used to anonymize email addresses and user targets (already done in base datasets)
        for word in element.split(" "):
            if "@" in word and ".com" in word or "gmail" in word or "yahoo" in word or ".fr" in word or ".ca" in word:
                word = ""
            elif word.startswith("@"):
                word = ""
            newElement.append(word)
        element = " ".join(newElement)
        # completely strips everything that is not in the french alphebet, a number, a tag, newline or space
        # any additional desired punctuation can be typed in and it will be excluded as well
        element = re.sub('\n', ' ', element)
        regex = re.compile('[^a-ÿ0-9 ]')
        element = re.sub(regex, '', element)
        # some characters are caused by encoding errors so are not removed by the regex
        element = element.translate(transtable)
        for word in element.split(" "):
            if word in freq.keys():
                freq[word] += 1
            else:
                freq[word] = 1
            if len(word) > 1:
                count += 1
    words = []
    mostFrequent = sorted(freq.items(), key=lambda x:x[1])
    for frequentWord in mostFrequent[-2:-52:-1]:
        words.append(frequentWord[0])

    return words

uniqPar = []
uniqQue = []
parisian = frequencycount("jasezClean.xml")
quebecois = frequencycount("smailfrClean.xml")

for word in parisian:
    if word not in quebecois:
        uniqPar.append(word)

for word in quebecois:
    if word not in parisian:
        uniqQue.append(word)

print("The words that are unique to the Quebecois corpus are: {}".format(uniqQue))
print("There are {} unique Quebecois words out of 1000".format(len(uniqQue)))
print("The words that are unique to the Parisian corpus are: {}".format(uniqPar))
print("There are {} unique Parisian words out of 1000".format(len(uniqPar)))

    # uniq = 0
    #
    # for value in freq.values():
    #     if value > 2:
    #         uniq += 1

    # print("The number of words in the corpus: {}".format(count))
    # print("The number of unique words in the corpus: {}".format(uniq))
    # print("The 50 most frequent words are")




