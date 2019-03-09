import scrapy
import json
import os
import re
from webcrawler.utils.helper import *


##This spider is for Ebay mobile only.
class MobilesSpider(scrapy.Spider):
    name = "mobiles"
    trans_table = {ord(c): None for c in u'\r\n\t'}
    accLabels = ["Operating System","Features","Brand", "Warranty","Network Technology","Storage Capacity", 
    "Color","RAM","Camera Resolution","Screen Size"]

    def HTMLFileURLGenerator(self, currentTargetHtmlFolder):
        
        urls = []
        if currentTargetHtmlFolder:
            for filename in os.listdir(currentTargetHtmlFolder):
                if (filename.endswith(".html")):
                    urls.append(os.path.join(currentTargetHtmlFolder,filename))
        return urls
       

    def start_requests(self):
        # urls = [
        #     'https://www.ebay.com/itm/Excellent-Samsung-Galaxy-S8-Plus-G955U-64-GB-Orchid-Gray-Verizon-GSM-Unlocked-/163407137164?hash=item260bd3098c',
        #     # 'file:///D:/Code/Python/ndsc2019/html/ebay/mobile/specs1.html'
        # ]
        self.rootPath = os.path.abspath(os.curdir)
        currModelIdRegex = r"^\d+_.*"
        self.htmlFolderPath = os.path.join(self.rootPath,"html","ebay","mobile3")
       
        for foldername in os.listdir(self.htmlFolderPath):
            matchObj = re.match(currModelIdRegex,foldername)
            if not matchObj:
                continue
            self.currentTargetHtmlFolder = os.path.join(self.htmlFolderPath,matchObj.group())
            urls = self.HTMLFileURLGenerator(self.currentTargetHtmlFolder)
            if not urls:
                return
            for url in urls:
                yield scrapy.Request(url=f"file:///{url}", callback=self.parse)
                break
            break

       

    def parse(self, response):
        #/tr/td[contains(@width,"50%")/text()]
        res = {}
        previousKey = ""
        nextIsTarget = False
        items = response.xpath("//div[@class='itemAttr']/*/table/tr/td")
        for item in items:
            itemText = item.get()
            if not itemText:
                continue
            label = item.css(".attrLabels").get()
            labelRes = getEnglishSentenseOnly(label)
        
            if labelRes:
                if labelRes.upper() in (name.upper() for name in self.accLabels):
                    res[labelRes] = []
                    previousKey = labelRes
                    nextIsTarget = True
                continue
            
            attribute = itemText
            attributeRes = getEnglishSentenseOnly(attribute)
            if attributeRes:
                  if nextIsTarget and previousKey:
                    res[previousKey].append(attributeRes)
                    nextIsTarget = False
                    previousKey = ""
             
        f = open("result.json","w+")
        f.write(json.dumps(res, indent=4, sort_keys=True))
        f.close()
        # for i in range(len(res)):
        #     f.write(res[i]+"\r\n")
        # f.close()
           

            
        # yield{
        #     'Brand': attribute.xpath("//tr/following-sibling::td[@class='attrLabels' and contains(.//test(),'Brand')]/td[contains(@width,'50%')/text()]").get(),
        # }