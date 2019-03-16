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

        if not currJsonObj: 
            return
        
        cameraList = currJsonObj["Camera"]
        res = firstTwoHighestDuplicatedTimesStringInDesc(cameraList)
        return res
    
    def processColorFamily(self, currJsonObj):

        if not currJsonObj:
            return

        colorFamily = currJsonObj["Color Family"]
        res = firstTwoHighestDuplicatedTimesStringInDesc(colorFamily)
        return res

    def storageCapacity(self, currJsonObj):

        if not currJsonObj:
            return 
        
        storageCapacity = currJsonObj["Storage Capacity"]
        res = firstTwoHighestDuplicatedTimesStringInDesc(storageCapacity)
        return res


    def generateCurrJsonOutputObj(self):
        currJsonOutputObj = {}
        



    def outputJson(self):

        myFile = open(self.finalJsonFilePath, 'w+')
        #first line 
        for filename in os.listdir(self.jsonRootFolder):
            filePath = os.path.join(self.jsonRootFolder,filename)
            with open (filePath) as f:
                self.targetModelData = json.load(f)
                res = self.generateResultArray()
               
                for item in res:
                    rowArray = ",".join(list(str(i) for i in list(item)))
                    myFile.write(f"{filename},{rowArray}\n")
        
        myFile.close()

        



