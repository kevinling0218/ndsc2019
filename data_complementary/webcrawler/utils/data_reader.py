import os
import pandas as pd

class trainDataPhoneModelReader:
    #class Arrtibute
    rootPath = ""
    filePath = ""
    modelIdList = []
    def __init__(self):
        self.rootPath = os.path.abspath(os.curdir)
        self.filePath = os.path.join(self.rootPath,"data","mobile_data_info_train_competition.csv")
        return
    
    def readTrainDataPhoneModelIdList(self):
        df_mobile_val = pd.read_csv('./data/mobile_data_info_train_competition.csv')
        self.modelIdList = df_mobile_val["Phone Model"].dropna().unique().astype(int)
        
        return 
