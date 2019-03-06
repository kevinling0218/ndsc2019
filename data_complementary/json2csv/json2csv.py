import os
import json
from webcrawler.utils.helper import *

class Json2Csv:
    #Attributes
    currProjectFolderPath = os.path.abspath(os.curdir)
    jsonRootFolder = os.path.join(currProjectFolderPath,"data_complementary","json2csv","json")
    trainJsonFile = os.path(currProjectFolderPath,"data","mobile_profile_train.json")
    targetModelId = -1
    trainJsonData = {}
    targetModelData = {}

    def __init__(self, modelId):
        self.targetModelId = modelId
        filePath = os.path.join(self.jsonRootFolder,f"{str(modelId)}.json")
        with open (filePath) as f:
            self.targetModelData = json.load(f)
        with open(self.trainJsonFile) as f:
            self.trainJsonData = json.load(f)
        return
    
    #OS string pipe
    def OSPipe(self):
        osStr = self.targetModelData["Operating System"]
        if not osStr:
            return ""
        lowerOSStr = osStr.lower().replace(" ", "")
        #Is IOS
        iosPotential = ["ios","apple"]
        if any(word in lowerOSStr for word in iosPotential):
            return 1
        #Is Android
        androidPotential = ["android","google"]
        if any(word in lowerOSStr for word in androidPotential):
            return 6
        #Is symbian
        symbianPotential = ["symbian"]
        if any(word in lowerOSStr for word in symbianPotential):
            return 2
        #Is windows
        windowsPotential = ["windows", "microsoft"]
        if any(word in lowerOSStr for word in windowsPotential):
            return 3
        #Is blackberry os
        blackBerryPotential = ["black", "berry", "blackberry"]
        if any(word in lowerOSStr for word in blackBerryPotential):
            return 5
        #Is samsung os
        samsungOsPotential = ["tizen", "linux", "samsung"]
        if any(word in lowerOSStr for word in samsungOsPotential):
            return 4
        #Is nokia os
        nokiaPotential = ["nokia","asha"]
        if any(word in lowerOSStr for word in nokiaPotential):
            return 0
        return ""
        
        
    #NetworkConnectionPipe
    def NetworkConnectionPipe(self):
        networkConnection = self.targetModelData["Network Connections"]
        if not networkConnection:
            return ""
        lowerNC = networkConnection.lower().replace(" ", "")
        #4g
        potential4G = ["4g","lte","four","forth"] 
        if any(word in lowerNC for word in potential4G):
            return 0
        #2g
        potential2G = ["2g", "gsm","two", "second"]
        if any(word in lowerNC for word in potential2G):
            return 1
        #3g
        potential3G = ["3g","three","third"]
        if any(word in lowerNC for word in potential3G):
            return 2
        #3.5g
        potential3dot5G = ["3.5g"]
        if any(word in lowerNC for word in potential3dot5G):
            return 3

        return ""

    #Memory RAM
    def RAMPipe(self):
        ram = self.targetModelData["Memory RAM"]
        if not ram:
            return ""
        lowerRAM = ram.lower().replace(" ", "")
        trainRamObj = self.trainJsonData["Memory RAM"]
        potentialObj ={
            "4gb": ["4g","4096","4000"],
            "2gb": ["2g", "2048", "2000"],
            "1.5gb":["1.5g","1536","1500"],
            "16gb": ["16g", "16384", "16000"],
            "512mb":["512m","0.5","0.512"],
            "8gb":["8g","8192","8000"],
            "3gb":["3g", "3072", "3000"],
            "10gb":["10g"],
            "1g":["1g","1024","1000"],
            "6gb": ["6g","6144"]
        }
        for k,v in trainRamObj.items():
            if any(word in lowerRAM for word in potentialObj[k]):
                return v
        
    
    #Brand
    def BrandPipe(self):
        brand = self.targetModelData["Brand"]
        if not brand:
            return ""
        lowerBrand = brand.lower().replace(" ","")
        trainBrandObj = self.trainJsonData["Brand"]
        for k,v in trainBrandObj.item():
            if any(word in lowerBrand for word in k.split()):
                return v

    #Warranty Period
    #1y 1m 1month 1 month 1year 1 year  
    def WarrantyPipe(self):
        warranty = self.targetModelData["Warranty Period"]
        if not warranty:
            return ""
        suspectNumber = 0
        lowerWarranty = warranty.lower().replace(" ","")
        trainWarrantyObj = self.trainJsonData["Warranty Period"]
        potentialNumbers = list(filter(str.isdigit, lowerWarranty))
        if (len(potentialNumbers) > 0):
            suspectNumber = int(potentialNumbers[0])
        
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
            
        if not resultKey:
            return trainWarrantyObj[resultKey]
        else:
            return ""
    
    #Storage Capacity
    def storageCapcityPipe(self):
        KEY = "Storage Capacity"
        storage = self.targetModelData[KEY]
        if not storage:
            return ""
        lowerStorage = storage.lower().replace(" ","")
        trainStorageObj = self.trainJsonData[KEY]
        #[:-1] means to remove the last character from the string
        for k,v in trainStorageObj.item():
            if any(k[:-1] in lowerStorage):
                return v
    
    #Color Family (skip)
    def colorFamily(self):
        return ""
    
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
        phoneScreen = self.targetModelData[KEY]
        if not phoneScreen:
            return ""
        lowerPhoneScreen = phoneScreen.lower().replace(" ","")
        suspectNumber = getFirstNumberOnly(lowerPhoneScreen)
        if suspectNumber <= 3.5:
            return 4
        elif suspectNumber > 3.5 and suspectNumber <= 4:
            return 1
        elif suspectNumber > 4 and suspectNumber <= 4.5:
            return 3
        elif suspectNumber > 4.5 and suspectNumber <= 5:
            return 0
        elif suspectNumber > 5 and suspectNumber < 5.5:
            return 5
        elif suspectNumber > 5.5 :
            return 2
      
        
            

        


        
        
            

                    
        



