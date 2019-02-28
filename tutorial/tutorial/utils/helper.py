import sys
import re

def cleanText(theText):
    return ''.join(c for c in theText if c not in '\r\t\n').strip()

def getEnglishSentenseOnly(theText):
    turn1 = re.sub("<.*?>", "", theText)
    turn2 = re.sub("[^a-zA-Z0-9 +]", "", turn1.strip())
    return turn2
# def add(value1, value2):
#     return value1 + value2

# result = add(3, 5)
# print(result)

