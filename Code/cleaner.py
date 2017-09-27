import re

setList = []
nonstandard = "«»¤¡♥°ºœ¨ùø§¹"
replace = "             "
transtable = str.maketrans(nonstandard, replace)

with open("smailfr.xml", "r", encoding='utf8') as x:
    for element in x:
        setList.append(element)

with open("Clean.xml", "w", encoding='utf8') as x:
    for element in setList:
        element = element.lower()
        # Uncomment to strip out tags as well, to recover raw text
        # element = re.sub(r'<.*?>', '', element)
        element = re.sub(r'https?:\/\/.*[]', 'removedurl', element)
        newElement = []
        # Used to anonymize email addresses and user targets (already done in base datasets)
        for word in element.split(" "):
            if "@" in word and ".com" in word or "gmail" in word or "yahoo" in word or ".fr" in word or ".ca" in word:
                word = "redactedemail"
            elif word.startswith("@"):
                word = "redactedusername"
            newElement.append(word)
        element = " ".join(newElement)
        # completely strips everything that is not in the french alphebet, a number, a tag, newline or space
        # any additional desired punctuation can be typed in and it will be excluded as well
        regex = re.compile('[^a-ÿ0-9<>\n ]')
        element = re.sub(regex, '', element)
        # some characters are caused by encoding errors so are not removed by the regex
        element = element.translate(transtable)
        x.write(element)

