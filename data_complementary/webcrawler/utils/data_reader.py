import os
import json
import pandas as pd

class trainDataPhoneModelReader:
    #class Arrtibute
    rootPath = ""
    filePath = ""
    modelIdList = []
    def __init__(self):
        self.rootPath = os.path.abspath(os.curdir)
        self.filePath = os.path.join(self.rootPath,"data","mobile_data_info_train_competition.csv")
        self.csvoutPath = os.path.join(self.rootPath,"data_complementary","webcrawler","utils","testoutput.csv")
        return

    def readTrainDataAll(self):
        df_mobile_val = pd.read_csv(self.filePath)
        return df_mobile_val

    def readTrainDataPhoneModelIdList(self):
        df_mobile_val = pd.read_csv('./data/mobile_data_info_train_competition.csv')
        self.modelIdList = df_mobile_val["Phone Model"].dropna().unique().astype(int)
        
        return 

    def readTrainDataDropPhoneModelNA(self):
        df_mobile_val = pd.read_csv(self.filePath).dropna(subset=['Phone Model'])
        #df_mobile_val.to_csv(self.csvoutPath, index=False)
        return


class JsonResultReader:

    def __init__(self):
        self.rootPath = os.path.abspath(os.curdir)
        self.jsonRootFolder = os.path.join(self.rootPath,"data_complementary","json2csv","json3")
    
    def getTargetDataByModelId(self,modelId):
        targetModelData = {}
        filename = f"{modelId}.json"
        filePath = os.path.join(self.jsonRootFolder,filename)
        with open (filePath) as f:
            targetModelData = json.load(f)
        
        return targetModelData
