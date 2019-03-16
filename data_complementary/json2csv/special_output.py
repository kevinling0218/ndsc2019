import os
import json
import operator
from webcrawler.utils.helper import *
class SpecialOutput:

    sample = {
        "1208": {
            "Camera":[2,4],
            "Color Family":[3,6],
            "Storage Capacity":[7,8]
        },
        "2261":{
            "Camera":[2,4],
            "Color Family":[3,6],
            "Storage Capacity":[7,8]
        }
    }

    def __init__(self):
        currProjectFolderPath = os.path.abspath(os.curdir)
        self.finalJsonFileName = "special.json"
        self.finalJsonFileFolder = os.path.join(currProjectFolderPath,"data_complementary","final")
        self.finalJsonFilePath = os.path.join(self.finalJsonFileFolder,self.finalJsonFileName)
        self.jsonRootFolder = os.path.join(currProjectFolderPath,"data_complementary","json2csv","json3")
        return

    #process camear
    #currJsonObj = {
    #           "Brand": "Sony",
    #           "Color Family": [
    #     "Black",
    #     "Black",
    #     "Black",
    #     "Silver",
    #     "Black",
    #     "Black",
    #     "Black",
    #     "Black"
    # ],
    # "Features": "Auto Focus",
    # "Phone Screen Size": "30"
    # }
    def processCamera(self, currJsonObj):

        res = []
        if not currJsonObj: 
            return res
        if "Camera" not in currJsonObj:
            return res
        cameraList = currJsonObj["Camera"]
        res = firstTwoHighestDuplicatedTimesStringInDesc(cameraList)
        return res
    
    def processColorFamily(self, currJsonObj):
        res = []
        if not currJsonObj:
            return res
        if "Color Family" not in currJsonObj:
            return res
        colorFamily = currJsonObj["Color Family"]
        res = firstTwoHighestDuplicatedTimesStringInDesc(colorFamily)
        return res

    def storageCapacity(self, currJsonObj):

        res = []
        if not currJsonObj:
            return res
        if "Storage Capacity" not in currJsonObj:
            return res 
        
        storageCapacity = currJsonObj["Storage Capacity"]
        res = firstTwoHighestDuplicatedTimesStringInDesc(storageCapacity)
        return res


    def generateCurrJsonOutputObj(self,currJsonObj):
        currJsonOutputObj = {}
  
        cameraList = self.processCamera(currJsonObj)
        colorFamilyList = self.processColorFamily(currJsonObj)
        storageCapacityList = self.storageCapacity(currJsonObj)
        
        currJsonOutputObj["Camera"] = cameraList
        currJsonOutputObj["Color Family"] = colorFamilyList
        currJsonOutputObj["Storage Capacity"] = storageCapacityList

        return currJsonOutputObj

        


    def outputJson(self):

        outObj = {}
        myFile = open(self.finalJsonFilePath, 'w+')
        #first line 
        for filename in os.listdir(self.jsonRootFolder):
            filePath = os.path.join(self.jsonRootFolder,filename)
            with open (filePath) as f:
                self.targetModelData = json.load(f)
                currObj = self.generateCurrJsonOutputObj(self.targetModelData)
                filenameWithoutExtention = os.path.splitext(filename)[0]
                outObj[filenameWithoutExtention] = currObj
               
        myFile.write(json.dumps(outObj, indent=4, sort_keys=True))
        myFile.close()

        



