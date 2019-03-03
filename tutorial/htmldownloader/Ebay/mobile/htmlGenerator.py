import os
import json
import urllib.request
import urllib.parse as urlparse
from urllib.parse import urlencode
from pprint import pprint
class keywordReader:

    #class Attribute
    attr = "test"
    rootPath = ""
    filePath = ""
    TARGET_KEY = "Phone Model"

     # Initializer / Instance Attributes
    def __init__(self):
        self.rootPath = os.path.abspath(os.curdir)
        self.filePath = os.path.join(self.rootPath,"dataset","mobile_profile_train.json")

    
    def readMobileModelDic(self):
        with open (self.filePath) as f:
            data = json.load(f)
        
        return data[self.TARGET_KEY]
        

class HTMLGenerator:

    htmlRoot = "https://www.ebay.com/sch/i.html"#?_nkw=
    #Folder naming convention is number_modelName
    def __init__(self):
        self.rootPath = os.path.abspath(os.curdir)
        self.folderPath = os.path.join(self.rootPath,"ebay","mobile")
        return
    
    def test1(self):
        keyword = keywordReader()
        modelDic = keyword.readMobileModelDic()
        #pprint(modelDic)
        for key,model in modelDic.items():
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
            ff = open("resultHTML.html","w+")
            ff.write(str(content, 'utf-8'))
            ff.close()
            break
        return
    
    def updateURLParams(self,paramsDic):
        url = self.htmlRoot

        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(paramsDic)

        url_parts[4] = urlencode(query)
        res = urlparse.urlunparse(url_parts)
        return res



htmlGen = HTMLGenerator()
htmlGen.test1()