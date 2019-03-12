import os
import json
import csv
import itertools
from webcrawler.utils.helper import *

class Json2Csv:
    #Attributes
    currProjectFolderPath = os.path.abspath(os.curdir)
    jsonRootFolder = os.path.join(currProjectFolderPath,"data_complementary","json2csv","json3")
    trainJsonFile = os.path.join(currProjectFolderPath,"data","mobile_profile_train.json")
    targetModelId = -1
    trainJsonData = {}
    targetModelData = {}
    result = []
    finalCSVFolder = os.path.join(currProjectFolderPath,"data_complementary","final")
    finalCSVName = "res_mobile_data_info_train.txt"

    def __init__(self):

        with open(self.trainJsonFile) as f:
            self.trainJsonData = json.load(f)

        #create final csv folder if its not exist
        if not os.path.exists(self.finalCSVFolder):
            os.makedirs(self.finalCSVFolder)
        return


    def setTargetModelData(self,targetModelData):
        self.targetModelData = targetModelData


    def generateResultArraySingle(self):
        itemIdStr = ""
        titleStr = ""
        imagePathStr = ""
        osStr = getFirstItemOfArray(self.OSPipe())
        feature = ""
        networkStr = getFirstItemOfArray(self.NetworkConnectionPipe())
        ramStr = getFirstItemOfArray(self.RAMPipe())
        brandStr = getFirstItemOfArray(self.BrandPipe())
        warrantyStr = getFirstItemOfArray(self.WarrantyPipe())
        storageCapcity = ""
        colorFamily = ""
        phoneModelStr = ""
        camera = ""
        phoneScreen = getFirstItemOfArray(self.phoneScreenPipe())

        resultArray = [itemIdStr,titleStr,imagePathStr, osStr,feature,networkStr,ramStr,brandStr,warrantyStr,storageCapcity,colorFamily,phoneModelStr,camera,phoneScreen]
        return resultArray


    def generateResultArray(self):

        osStrs = self.OSPipe()
        features = []
        networkStrs = self.NetworkConnectionPipe()
        ramStrs = self.RAMPipe()
        brandStrs = self.BrandPipe()
        warrantyStrs = self.WarrantyPipe()
        #multi
        storageCapcities = self.storageCapcityPipe()
        #multi
        colorFamilies = self.colorFamilyPipe()
        #multi
        cameras = self.cameraPipe()
        phoneScreens = self.phoneScreenPipe()
        
        iterables = [osStrs,features,brandStrs, warrantyStrs, networkStrs, storageCapcities, colorFamilies,ramStrs,cameras,phoneScreens]
        for iterarray in iterables:
            fillNAArray(iterarray)
        resultArray = list(itertools.product(*iterables))

        return resultArray


    def outputFinalCSV(self):
        
      
        myFile = open(self.finalCSVName, 'w+')
        #first line
        myFile.write("Phone Model,Operating System,Features,Brand,Warranty Period,Network Connections,Storage Capacity,Color Family,Memory RAM,Camera,Phone Screen Size\n")  
        for filename in os.listdir(self.jsonRootFolder):
            filePath = os.path.join(self.jsonRootFolder,filename)
            with open (filePath) as f:
                self.targetModelData = json.load(f)
                res = self.generateResultArray()
               
                for item in res:
                    rowArray = ",".join(list(str(i) for i in list(item)))
                    myFile.write(f"{filename},{rowArray}\n")
        
        myFile.close()
                # with myFile:  
                #     writer = csv.writer(myFile)
                #     for item in res:
                #         rowArray = list(str(i) for i in list(item))
                #         writer.writerows(rowArray)
        

     
       
    
    #OS string pipe
    def OSPipe(self):
        KEY = "Operating System"
        res_set = set()
        if KEY not in self.targetModelData:
            return list(res_set)
        osStr = removeDuplicateItemFromArray(self.targetModelData[KEY])
        if not osStr:
            return list(res_set)
        
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
                res_set.add(v)

        return list(res_set)
        
    #NetworkConnectionPipe
    def NetworkConnectionPipe(self):
        KEY = "Network Connections"
        res_set = set()
        if KEY not in self.targetModelData:
            return list(res_set)
        networkConnection = removeDuplicateItemFromArray(self.targetModelData[KEY])
        if not networkConnection:
            return list(res_set)
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
                res_set.add(v)

        return list(res_set)

    #Memory RAM
    def RAMPipe(self):

        KEY = "Memory RAM"
        res_set = set()
        if KEY not in self.targetModelData:
            return list(res_set)
        ram = removeDuplicateItemFromArray(self.targetModelData[KEY])
        if not ram:
            return list(res_set)
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
                res_set.add(v)
        
        return list(res_set)
        
    
    #Brand
    def BrandPipe(self):

        KEY = "Brand"
        res_set = set()
        if KEY not in self.targetModelData:
            return list(res_set)
        brand = removeDuplicateItemFromArray(self.targetModelData[KEY])
        if not brand:
            return list(res_set)
        lowerBrand = brand.lower().replace(" ","")
        trainBrandObj = self.trainJsonData[KEY]
        for k,v in trainBrandObj.items():
            if any(word in lowerBrand for word in k.split()):
                res_set.add(v)
        return list(res_set)

    #Warranty Period
    #1y 1m 1month 1 month 1year 1 year  
    def WarrantyPipe(self):
        KEY = "Warranty Period"
        res_set = set()
        if KEY not in self.targetModelData:
            return list(res_set)
        warranty = removeDuplicateItemFromArray(self.targetModelData[KEY])
        if not warranty:
            return list(res_set)
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
            return res_set.add(trainWarrantyObj[resultKey])

        return list(res_set)
    
    #Storage Capacity
    def storageCapcityPipe(self):
        KEY = "Storage Capacity"
        res_set = set()
        if KEY not in self.targetModelData:
            return list(res_set)
        storageList = removeDuplicateItemFromArray(self.targetModelData[KEY])
        if not storageList or len(storageList) == 0:
            return list(res_set)
            
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
                        res_set.add(v)
                
                #When current unit is M
                if isLowerStorageContainM and isTrainContainsM:
                    if lowerStorageNumberOnly == trainNumber:
                        res_set.add(v)

        return list(res_set)
        
    
    #Color Family (skip)
    def colorFamilyPipe(self):
        res_set = set()
        KEY = "Color Family"
        if KEY not in self.targetModelData:
            return list(res_set)
        colorList = removeDuplicateItemFromArray(self.targetModelData[KEY])
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
        res_set = set()
        KEY = "Camera"
        if KEY not in self.targetModelData:
            return list(res_set)
        cameraList = removeDuplicateItemFromArray(self.targetModelData[KEY])
        if not cameraList or len(cameraList) == 0:
            return list(res_set)
    
        trainCameraObj = self.trainJsonData[KEY]
        ##Append single slot or dual slot
        if len(cameraList) == 1:
            res_set.add(6)
        elif len(cameraList) > 1:
            res_set.add(1)

        for idx, val in enumerate(cameraList):    
            lowerCamera = val.lower().replace(" ","")
            suspectNumber = getFirstNumberOnly(lowerCamera)
            for numText in trainCameraObj:
                if (suspectNumber == getFirstNumberOnly(numText)):
                   res_set.add(trainCameraObj[numText])
        return list(res_set)

    #Phone Screen Size
    def phoneScreenPipe(self):
        KEY = "Phone Screen Size"
        res_set = set()
        if KEY not in self.targetModelData:
            return list(res_set)
        phoneScreen = removeDuplicateItemFromArray(self.targetModelData[KEY])
        if not phoneScreen:
            return list(res_set)
        lowerPhoneScreen = phoneScreen.lower().replace(" ","")
        suspectNumber = getFirstNumberOnly(lowerPhoneScreen)
        if suspectNumber <= 3.5:
            res_set.add(4)
        elif suspectNumber > 3.5 and suspectNumber <= 4:
            res_set.add(1)
        elif suspectNumber > 4 and suspectNumber <= 4.5:
            res_set.add(3)
        elif suspectNumber > 4.5 and suspectNumber <= 5:
            res_set.add(0)
        elif suspectNumber > 5 and suspectNumber < 5.5:
            res_set.add(5)
        elif suspectNumber > 5.5 :
            res_set.add(2)
        return list(res_set)
        
            
# json2csv = Json2Csv(1208)
# json

        
        
            

                    
        



