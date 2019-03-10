import sys
import re
from decimal import Decimal

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

    findRes = re.search(r'\d+\.*\d{1}', theText)
    if findRes:
        potentialNumber = findRes.group()
        if potentialNumber:
            return Decimal(potentialNumber)
    
    return 0

def isContainStr(theText, str):
    res = theText.find(str)
    return True if res != -1 else False


def fillNAArray(theArray):

    if len(theArray) == 0:
        theArray.append(-1)
    
    return

def removeDuplicateItemFromArray(theArray):
    if not isinstance(theArray,list):
        return theArray
    mylist = list(dict.fromkeys(theArray))
    return mylist



