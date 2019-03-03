import scrapy
import json
from tutorial.utils.helper import *

##This spider is for Ebay mobile only.
class MobilesSpider(scrapy.Spider):
    name = "mobiles"
    trans_table = {ord(c): None for c in u'\r\n\t'}
    accLabels = ["Brand","Network Technology", "Model", "Processor","Style","Storage Capacity","Manufacturer Color"
    "Color","Memory Card Type", "Network","Camera Resolution","Screen Size"]
    
    def start_requests(self):
        urls = [
            #'https://www.ebay.com/itm/Excellent-Samsung-Galaxy-S8-Plus-G955U-64-GB-Orchid-Gray-Verizon-GSM-Unlocked-/163407137164?hash=item260bd3098c',
            'file:///D:/Code/Python/ndsc2019/html/ebay/mobile/specs1.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

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