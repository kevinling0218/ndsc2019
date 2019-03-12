import os
import pandas as pd
from webcrawler.utils.helper import *
from webcrawler.utils.data_reader import trainDataPhoneModelReader,JsonResultReader
from json2csv.json2csv import Json2Csv
class TrainModifier:
    #Attributes
    itemId_KEY = "itemid"
    title_KEY = "title"
    imagePath_KEY = "image_path"
    OS_KEY = "Operating System"
    
    
    PhoneModel_KEY = "Phone Model"
    def __init__(self):
        trainReader = trainDataPhoneModelReader()
        self.df_mobile_val = trainReader.readTrainDataAll()
        #self.df_mobile_val = trainReader.readTestTrainDataAll()
        self.json2csv = Json2Csv()
        self.jsonResultReader = JsonResultReader()
        self.rootPath = os.path.abspath(os.curdir)
        self.csvoutPath = os.path.join(self.rootPath,"data_complementary","webcrawler","utils","testoutput.csv")
        return

    def modifyDataFrame(self):
        for index, row in self.df_mobile_val.iterrows():
            if not pd.isna(row[self.PhoneModel_KEY]):
                phoneModelId = row[self.PhoneModel_KEY]
                phoneModelIdStr = str(int(phoneModelId))
                targetModelData = self.jsonResultReader.getTargetDataByModelId(phoneModelIdStr)
                self.json2csv.setTargetModelData(targetModelData)
                #osStr,feature,networkStr,ramStr,brandStr,warrantyStr,storageCapcity,colorFamily,camera,phoneScreen
                #Operating System,Features,Network Connections,Memory RAM,Brand,Warranty Period,Storage Capacity,Color Family,Phone Model,Camera,Phone Screen Size
                resultArrayForCurrRow = self.json2csv.generateResultArraySingle()
                self.completeDataFrameRow(index,row,resultArrayForCurrRow)
        
        #Ready for final answer
        self.df_mobile_val.to_csv(self.csvoutPath, index=False)

    
    def modifyDataFrameTest(self):
        phoneModelIdStr = "1526"
        targetModelData = self.jsonResultReader.getTargetDataByModelId(phoneModelIdStr)
        self.json2csv.setTargetModelData(targetModelData)
        resultArrayForCurrRow = self.json2csv.generateResultArraySingle()
        row = self.df_mobile_val.loc[0]
        oldRow = row
        self.completeDataFrameRow(0,row,resultArrayForCurrRow)
        newRow = self.df_mobile_val.loc[0]

        print(newRow)





    def completeDataFrameRow(self,currIndex,currRow, resultArrayRow):
        #osStr,feature,networkStr,ramStr,brandStr,warrantyStr,storageCapcity,colorFamily,camera,phoneScreen
        #Operating System,Features,Network Connections,Memory RAM,Brand,Warranty Period,Storage Capacity,Color Family,Phone Model,Camera,Phone Screen Size
        columnName = ["itemid","title","image_path","Operating System","Features","Network Connections","Memory RAM","Brand","Warranty Period","Storage Capacity","Color Family","Phone Model",
        "Camera","Phone Screen Size"]
        for index, key in enumerate(currRow):
            #note index === 11 is phone model
            if index == 11:
                continue
            #if curr column data is na
            if pd.isna(key) and resultArrayRow[index]:
                # self.df_mobile_val.set_value(currIndex,columnName[index], resultArrayRow[index])
                self.df_mobile_val.at[currIndex,columnName[index]] = resultArrayRow[index]


            




    

