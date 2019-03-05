import os
import json
class Json2Csv:
    #Attributes
    currProjectFolderPath = os.path.abspath(os.curdir)
    jsonRootFolder = os.path.join(currProjectFolderPath,"data_complementary","json2csv","json")
    targetModelId = -1
    targetModelData = {}

    def __init__(self, modelId):
        self.targetModelId = modelId
        filePath = os.path.join(self.jsonRootFolder,f"{str(modelId)}.json")
        with open (filePath) as f:
            self.targetModelData = json.load(f)
        return
    
    def parseOS(self):
        osStr = self.targetModelData["Operating System"]
        if not osStr:
            return ""
        lowerOSStr = osStr.lower()
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
        
        
