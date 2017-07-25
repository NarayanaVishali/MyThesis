#!/usr/bin/env python

import re

# This function removes new line & return carriages from tweets
def stripNewLineAndReturnCarriage(tweetText):
    return tweetText.replace('\n', ' ').replace('\r', '').strip().lstrip()

# This function is used to remove all the URL's in a tweet
def removeURL(tweetText):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweetText)

# This function is used to remove user mentions in a tweet
def removeUserMentions(tweetText):
    return re.sub('@[^\s]+','',tweetText)

# This function replaces words with repeating 'n' or more same characters with a single character
def replaceRepeatedCharacters(tweetText):
    return re.sub(r"(.)\1{3,}",r"\1", tweetText)

# This function is used to convert multiple white spaces into a single white space
def convertMultipleWhiteSpacesToSingleWhiteSpace(tweetText):
    return re.sub('[\s]+', ' ', tweetText)

# This function replaces any hash tag in a tweet with the word
def replaceHashTagsWithWords (tweetText):
    return re.sub(r'#([^\s]+)', r'\1', tweetText)

# This function is used to chack if a word occurs in a tweet
def isWordInTweet(tweetText, FilterWord, splitBy):
    flag = False
    strArray = tweetText.lower().split(splitBy)
    print strArray
    for word in strArray:
        if FilterWord.lower() == word.lower():
            flag = True
            break
    return flag

# This function is used to chack if a word occurs in a tweet
def isArrayOfFilterWordsInTweet(tweetText, filterWords, tweetSplitBy, filterWordSplitBy):
    flag = False
    wordsArray = tweetText.lower().split(tweetSplitBy)
    filterWordsArray = filterWords.lower().split(filterWordSplitBy)
    for word in wordsArray:
        for filterWord in filterWordsArray:
            if filterWord.lower() == word.lower():
                flag = True
                break
    return flag

# Extract date from timestamp
def extractDateFromTimestamp(timestamp):
    from dateutil import parser
    d = parser.parse(timestamp.strip().lstrip())
    return str(d.date())

# Extract time from timestamp
def extractTimeFromTimestamp(timestamp):
    from dateutil import parser
    d = parser.parse(timestamp.strip().lstrip())
    return str(d.time())

# Convert String to timestamp
def convertStringToTimestamp(timestamp):
    from dateutil import parser
    return parser.parse(timestamp.strip().lstrip())

# This function is used to split a string and return an array based on a passed delimiter
def splitStringAndReturnArray(text, delimiter):
    return text.lstrip().strip().split(delimiter)

# This function removes items from a list in a tweet text
def removeItemsInTweetContainedInAList(tweet_text,stop_words,splitBy):
    wordsArray = splitStringAndReturnArray(tweet_text,splitBy)
    StopWords = list(set(wordsArray).intersection(set(stop_words)))
    return_str=""
    for word in wordsArray:
        if word not in StopWords:
            return_str += word + splitBy
    return return_str.strip().lstrip()

# This function reads a file and returns its contents as an array
def readFileandReturnAnArray(fileName, readMode, isLower):
    myArray=[]
    with open(fileName, readMode) as readHandle:
        for line in readHandle.readlines():
            lineRead = line
            if isLower:
                lineRead = lineRead.lower()
            myArray.append(lineRead.strip().lstrip())
    readHandle.close()
    return myArray