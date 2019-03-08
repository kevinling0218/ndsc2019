import os
import json
import urllib
import requests
import urllib.parse as urlparse
from urllib.parse import urlencode
from pprint import pprint
from scrapy.selector import Selector
from bs4 import BeautifulSoup as bs
from webcrawler.utils.data_reader import trainDataPhoneModelReader

class keywordReader:

    #class Attribute
    attr = "test"
    rootPath = ""
    filePath = ""
    TARGET_KEY = "Phone Model"

     # Initializer / Instance Attributes
    def __init__(self):
        self.rootPath = os.path.abspath(os.curdir)
        self.filePath = os.path.join(self.rootPath,"data","mobile_profile_train.json")

    
    def readMobileModelDic(self):
        with open (self.filePath) as f:
            data = json.load(f)
        
        return data[self.TARGET_KEY]
        

class HTMLGenerator:

    #9355 means only search phone device  _nkw = "" <- accurate match  _nkw= <- similarity match
    htmlRoot = "https://www.ebay.com/sch/9355/i.html"#?_nkw=
    itemListURLXpathSchema = "//*[@id='mainContent' and contains(@class,'srp-main-content')]//ul[contains(@class,'srp-results')]//li[contains(@class,'s-item')]//a[contains(@class,'s-item__link')]/@href"
    #Folder naming convention is number_modelName
    def __init__(self):
        self.rootPath = os.path.abspath(os.curdir)
        self.folderPath = os.path.join(self.rootPath,"html","ebay","mobile2")

        trainReader = trainDataPhoneModelReader()
        trainReader.readTrainDataPhoneModelIdList()
        self.modelIdList = trainReader.modelIdList
        return
    
    def test1(self):
        keyword = keywordReader()
        modelDic = keyword.readMobileModelDic()
        #pprint(modelDic)
        for key,model in modelDic.items():
            if not model in self.modelIdList: 
                continue 
            #create a new folder
            currFolderName = f'{model}_{key}'
            newFolderPath = os.path.join(self.folderPath,currFolderName)
            if not os.path.exists(newFolderPath):
                os.makedirs(newFolderPath)
            
            #Download the top 10 result html if has
            opener = urllib.request.FancyURLopener({})
            url = self.updateURLParams({"_nkw": key})
            f = opener.open(url)
            content = f.read()
            f.close()
            #ul[contains(@class,'srp-results')]
            #li[contains(@class,'s-item__link')]
            #items.xpath("//*[@id='mainContent' and contains(@class,'srp-main-content')]//ul[contains(@class,'srp-results')]//li[contains(@class,'s-item')]//a[contains(@class,'s-item__link')]/@href")
            #https://www.ebay.com/itm/Samsung-Samsung-gear-S2-smartwatch-sports-black/123163937956?hash=item1cad248ca4:g:2jwAAOSw9mFbD7VD
            items = Selector(text=str(content,'utf-8')).xpath("//*[@id='mainContent' and contains(@class,'srp-main-content')]//ul[contains(@class,'srp-results')]//li[contains(@class,'s-item')]")
            top10Counter = 10
            for idx, item in enumerate (items):
                if top10Counter <= 0:
                    break
                currHref = item.xpath(".//a[@class='s-item__link']/@href").get()
                newFilePath = os.path.join(newFolderPath,f"{currFolderName}_{str(idx + 1)}.html")
                if not currHref:
                    break
                ff = requests.get(currHref)
                currContent = ff.text
                fileWriter = open(newFilePath,"w+",encoding="utf-8")
                soup = bs(currContent)      
                prettyHTML = soup.prettify()
                fileWriter.write(prettyHTML)
                fileWriter.close()
                top10Counter-=1
        return
    
    def updateURLParams(self,paramsDic):
        url = self.htmlRoot

        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(paramsDic)

        url_parts[4] = urlencode(query)
        res = urlparse.urlunparse(url_parts)
        return res

