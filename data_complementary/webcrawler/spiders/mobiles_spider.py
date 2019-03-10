import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import json
import os
import re
import operator
from webcrawler.utils.helper import *
from webcrawler.utils.pipe import*


##This spider is for Ebay mobile only.
class MobilesSpider(scrapy.Spider):
    name = "mobiles"
    trans_table = {ord(c): None for c in u'\r\n\t'}
    accLabels = ["Operating System","Features","Brand", "Warranty","Network Technology","Storage Capacity", 
    "Color","RAM","Camera Resolution","Screen Size"]
    res = {}
    rootPath = os.path.abspath(os.curdir)
    destinationJsonFolder = os.path.join(rootPath,"data_complementary","json2csv","json3")
    counter = 0 
    def HTMLFileURLGenerator(self, currentTargetHtmlFolder):
        
        urls = []
        if currentTargetHtmlFolder:
            for filename in os.listdir(currentTargetHtmlFolder):
                if (filename.endswith(".html")):
                    urls.append(os.path.join(currentTargetHtmlFolder,filename))
                else:
                    test2 = 1
            if len(os.listdir(currentTargetHtmlFolder)) == 0:
                test3 = 1
        else:
            test = 1 
        return urls
       
    def __init__(self):
         dispatcher.connect(self.engine_stopped, signals.engine_stopped)

    def engine_stopped(self):
        #print (self.res)
        #make res dic into destintation json file
        self.transformRes()
        if not os.path.exists(self.destinationJsonFolder):
            os.makedirs(self.destinationJsonFolder)
        for k,v in self.res.items():
            newFilePath = os.path.join(self.destinationJsonFolder,f"{str(k)}.json")
            f = open(newFilePath,"w+")
            f.write(json.dumps(v, indent=4, sort_keys=True))
            f.close()

    def transformRes(self):
        tempRes = {}
        for k,v in self.res.items():
            tempRes[k] = {}
            if isinstance(v,dict):
                for key,value in v.items():
                    if isinstance(value,list):
                        tempRes[k][key] = value
                    elif isinstance(value,dict):
                        highestKey = max(value.items(), key=operator.itemgetter(1))[0]
                        tempRes[k][key] = highestKey
            # else if isinstance(v, list):
            #     tempRes[k][]
        self.res = tempRes
        

    def start_requests(self):
        # urls = [
        #     'https://www.ebay.com/itm/Excellent-Samsung-Galaxy-S8-Plus-G955U-64-GB-Orchid-Gray-Verizon-GSM-Unlocked-/163407137164?hash=item260bd3098c',
        #     # 'file:///D:/Code/Python/ndsc2019/html/ebay/mobile/specs1.html'
        # ]
        self.rootPath = os.path.abspath(os.curdir)
        currModelIdRegex = r"^(\d+)_.*"
        self.htmlFolderPath = os.path.join(self.rootPath,"html","ebay","mobile3")
       
        test = os.listdir(self.htmlFolderPath)
        for foldername in os.listdir(self.htmlFolderPath):
            matchObj = re.match(currModelIdRegex,foldername)
            if not matchObj:
                continue
            self.currentTargetHtmlFolder = os.path.join(self.htmlFolderPath,matchObj.group())
            urls = self.HTMLFileURLGenerator(self.currentTargetHtmlFolder)
            if not urls:
                continue
            currModelId = matchObj.group(1)
            for url in urls:
                request = scrapy.Request(url=f"file:///{url}", callback=self.parse)
                request.meta['id'] = currModelId
                yield request

            # counter-=1
            # if counter == 0:
            #     break
            self.counter+=1

    
   

    def parse(self, response):
        #/tr/td[contains(@width,"50%")/text()]
        currId = response.meta['id']
        currURL = response.request.url
        if currId not in self.res:
            self.res [currId] = {}

        currRes = self.res[currId]
        previousKey = ""
        nextIsTarget = False
        items = response.xpath("//div[@class='itemAttr']/*/table/tr/td")
        for item in items:
            itemText = item.get()
            if not itemText:
                continue
            label = item.css(".attrLabels").get()
            labelRes = getEnglishSentenseOnly(label)
            attribute = itemText
            attributeRes = getEnglishSentenseOnly(attribute)
        
            if labelRes:
                if labelRes.upper() in (name.upper() for name in self.accLabels):
                    shopeeKey = ebayJsonKeyPipe(labelRes)
                    #currRes[shopeeKey] = { }
                    previousKey = shopeeKey
                    nextIsTarget = True
                continue
            
    
            if attributeRes:
                  if nextIsTarget and previousKey:
                    
                    isShopeeKeyArray = isShopeeKeyArrayValue(previousKey)
                    if isShopeeKeyArray:
                        if (previousKey not in currRes):
                            currRes[previousKey] = []
                        currRes[previousKey].append(attributeRes)
                    else:
                        if (previousKey not in currRes):
                            currRes[previousKey] = {}
                        if (attributeRes in currRes[previousKey]):
                            currRes[previousKey][attributeRes] += 1
                        else:
                            currRes[previousKey][attributeRes] = 1
                    nextIsTarget = False
                    previousKey = ""
             
        # f = open("result.json","w+")
        # f.write(json.dumps(res, indent=4, sort_keys=True))
        # f.close()
        # for i in range(len(res)):
        #     f.write(res[i]+"\r\n")
        # f.close()
        #print (currRes)

            
        # yield{
        #     'Brand': attribute.xpath("//tr/following-sibling::td[@class='attrLabels' and contains(.//test(),'Brand')]/td[contains(@width,'50%')/text()]").get(),
        # }