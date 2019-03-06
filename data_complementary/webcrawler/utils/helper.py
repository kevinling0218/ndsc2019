import sys
import re

def cleanText(theText):
    return ''.join(c for c in theText if c not in '\r\t\n').strip()

def getEnglishSentenseOnly(theText):
    if not theText:
        return
    turn1 = re.sub("<.*?>", "", theText)
    turn2 = re.sub("[^a-zA-Z0-9 +]", "", turn1.strip())
    return turn2


def getFirstNumberOnly(theText):
    if not theText:
        return
    suspectNumber = 0
    potentialNumbers = list(filter(str.isdigit, theText))
    if (len(potentialNumbers) > 0):
        suspectNumber = int(potentialNumbers[0])
    return suspectNumber




