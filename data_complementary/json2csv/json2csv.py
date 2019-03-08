import os
import json
import itertools
from webcrawler.utils.helper import *

class Json2Csv:
    #Attributes
    currProjectFolderPath = os.path.abspath(os.curdir)
    jsonRootFolder = os.path.join(currProjectFolderPath,"data_complementary","json2csv","json")
    trainJsonFile = os.path.join(currProjectFolderPath,"data","mobile_profile_train.json")
    targetModelId = -1
    trainJsonData = {}
    targetModelData = {}
    result = []

    def __init__(self, modelId):
        self.targetModelId = modelId
        filePath = os.path.join(self.jsonRootFolder,f"{str(modelId)}.json")
        with open (filePath) as f:
            self.targetModelData = json.load(f)
        with open(self.trainJsonFile) as f:
            self.trainJsonData = json.load(f)

        self.generateResultArray()
        return

    def generateResultArray(self):

        osStrs = self.OSPipe()
        networkStrs = self.NetworkConnectionPipe()
        ramStrs = self.RAMPipe()
        brandStrs = self.BrandPipe()
        warrantyStrs = self.WarrantyPipe()
        storageCapcities = self.storageCapcityPipe()
        colorFamilies = self.colorFamilyPipe()
        cameras = self.cameraPipe()
        phoneScreens = self.phoneScreenPipe()
        
        iterables = [osStrs,networkStrs, ramStrs,brandStrs,warrantyStrs,storageCapcities,colorFamilies,cameras,phoneScreens]
        for iterarray in iterables:
            fillNAArray(iterarray)
        resultArray = list(itertools.product(*iterables))

        return resultArray
    
    #OS string pipe
    def OSPipe(self):
        KEY = "Operating System"
        res = []
        osStr = self.targetModelData[KEY]
        if not osStr:
            return res
        
        lowerOS = osStr.lower().replace(" ","")
        trainOSObj = self.trainJsonData[KEY]
        potentialObj ={
            "ios": ["ios","apple"],
            "android": ["android","google"],
            "symbian": ["symbian"],
            "windows": ["windows", "microsoft"],
            "blackberry os": ["black", "berry", "blackberry"],
            "samsung os":["tizen", "linux", "samsung"],
            "nokia os":["nokia","asha"]
        }
        for k,v in trainOSObj.items():
            if any(word in lowerOS for word in potentialObj[k]):
                res.append(v)

        return res
        
    #NetworkConnectionPipe
    def NetworkConnectionPipe(self):
        KEY = "Network Connections"
        res = []
        networkConnection = self.targetModelData[KEY]
        if not networkConnection:
            return res
        lowerNC = networkConnection.lower().replace(" ", "")
        trainNCObj = self.trainJsonData[KEY]
        potentialObj = {
            "4g" : ["4g","lte","four","forth"],
            "2g" : ["2g", "gsm","two", "second"],
            "3g" : ["3g","three","third"],
            "3.5g" : ["3.5g"]
        }
        for k,v in trainNCObj.items():
            if any(word in lowerNC for word in potentialObj[k]):
                res.append(v)

        return res

    #Memory RAM
    def RAMPipe(self):

        KEY = "Memory RAM"
        res = []
        ram = self.targetModelData[KEY]
        if not ram:
            return res
        lowerRAM = ram.lower().replace(" ", "")
        trainRamObj = self.trainJsonData[KEY]
        potentialObj ={
            "4gb": ["4g","4096","4000"],
            "2gb": ["2g", "2048", "2000"],
            "1.5gb":["1.5g","1536","1500"],
            "16gb": ["16g", "16384", "16000"],
            "512mb":["512m","0.5","0.512"],
            "8gb":["8g","8192","8000"],
            "3gb":["3g", "3072", "3000"],
            "10gb":["10g"],
            "1gb":["1g","1024","1000"],
            "6gb": ["6g","6144"]
        }
        for k,v in trainRamObj.items():
            if any(word in lowerRAM for word in potentialObj[k]):
                res.append(v)
        
        return res
        
    
    #Brand
    def BrandPipe(self):

        KEY = "Brand"
        res = []
        brand = self.targetModelData[KEY]
        if not brand:
            return res
        lowerBrand = brand.lower().replace(" ","")
        trainBrandObj = self.trainJsonData[KEY]
        for k,v in trainBrandObj.items():
            if any(word in lowerBrand for word in k.split()):
                res.append(v)
        return res

    #Warranty Period
    #1y 1m 1month 1 month 1year 1 year  
    def WarrantyPipe(self):
        KEY = "Warranty Period"
        res = []
        warranty = self.targetModelData[KEY]
        if not warranty:
            return res
        suspectNumber = 0
        lowerWarranty = warranty.lower().replace(" ","")
        trainWarrantyObj = self.trainJsonData[KEY]
        suspectNumber = getFirstNumberOnly(lowerWarranty)
        
        resultKey = ""
        if "month" in lowerWarranty:
            if suspectNumber > 1:
                resultKey = f"{suspectNumber} months" 
            elif suspectNumber == 1:
                resultKey = f"{suspectNumber} month"
        
 
        if "year" in lowerWarranty:
            if suspectNumber > 1:
                resultKey = f"{suspectNumber} years"
            elif suspectNumber == 1:
                resultKey = f"{suspectNumber} year"
            
        if resultKey and resultKey in trainWarrantyObj:
            return res.append(trainWarrantyObj[resultKey])

        return res
    
    #Storage Capacity
    def storageCapcityPipe(self):
        KEY = "Storage Capacity"
        res = []
        storageList = self.targetModelData[KEY]
        if not storageList or len(storageList) == 0:
            return res
            
        trainStorageObj = self.trainJsonData[KEY]
        for idx,val in enumerate(storageList):
            lowerStorage = val.lower().replace(" ","")
            lowerStorageNumberOnly = getFirstNumberOnly(lowerStorage)
            isLowerStorageContainG = isContainStr(lowerStorage,'g')
            isLowerStorageContainM = isContainStr(lowerStorage,'m')
            #[:-1] means to remove the last character from the string
            for k,v in trainStorageObj.items():
                trainNumber = getFirstNumberOnly(k)
                isTrainContainsG = isContainStr(k, 'g')
                isTrainContainsM = isContainStr(k, 'm')
                
                #When current unit is G
                if isLowerStorageContainG and isTrainContainsG:
                    if lowerStorageNumberOnly == trainNumber:
                        res.append(v)
                
                #When current unit is M
                if isLowerStorageContainM and isTrainContainsM:
                    if lowerStorageNumberOnly == trainNumber:
                        res.append(v)

        return res
        
    
    #Color Family (skip)
    def colorFamilyPipe(self):
        res_set = set()
        KEY = "Color Family"
        colorList = self.targetModelData[KEY]
        if not colorList or len(colorList) == 0:
            return list(res_set)
        
        trainColorObj = self.trainJsonData[KEY]
        for idx, val in enumerate(colorList):
            lowColor = val.lower().replace(" ","")
            for colorTexts in trainColorObj:
                colorText = ""
                colorTextsArr = colorTexts.split(" ")
                if len(colorTextsArr) > 1:
                    colorText = colorTextsArr[1]
                else:
                    colorText = colorTextsArr[0]
                if colorText in lowColor:
                    res_set.add(trainColorObj[colorTexts])
        
        return list(res_set)
    
    #Camera
    #Priority list = 
    # [9,6,1,8,5,2,12,13,7,3]
    # [13mp,single camera,dua slot,16mp,8mp,5mp,2mp, 20mp,24mp,3mp]
    #From pandas histogram
    #Return value is an array(list)
    def cameraPipe(self):
        res = []
        KEY = "Camera"
        cameraList = self.targetModelData[KEY]
        if not cameraList or len(cameraList) == 0:
            return res
    
        trainCameraObj = self.trainJsonData[KEY]
        ##Append single slot or dual slot
        if len(cameraList) == 1:
            res.append(6)
        elif len(cameraList) > 1:
            res.append(1)

        for idx, val in enumerate(cameraList):    
            lowerCamera = val.lower().replace(" ","")
            suspectNumber = getFirstNumberOnly(lowerCamera)
            for numText in trainCameraObj:
                if (suspectNumber == getFirstNumberOnly(numText)):
                    res.append(trainCameraObj[numText])
        return res

    #Phone Screen Size
    def phoneScreenPipe(self):
        KEY = "Phone Screen Size"
        res = []
        phoneScreen = self.targetModelData[KEY]
        if not phoneScreen:
            return res
        lowerPhoneScreen = phoneScreen.lower().replace(" ","")
        suspectNumber = getFirstNumberOnly(lowerPhoneScreen)
        if suspectNumber <= 3.5:
             res.append(4)
        elif suspectNumber > 3.5 and suspectNumber <= 4:
             res.append(1)
        elif suspectNumber > 4 and suspectNumber <= 4.5:
             res.append(3)
        elif suspectNumber > 4.5 and suspectNumber <= 5:
             res.append(0)
        elif suspectNumber > 5 and suspectNumber < 5.5:
             res.append(5)
        elif suspectNumber > 5.5 :
             res.append(2)
        return res
        
            
# json2csv = Json2Csv(1208)
# json

        
        
            

                    
        



