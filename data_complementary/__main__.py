# from json2csv.json2csv import *
# json2csv = Json2Csv(1208)


# Import modules
# import pandas as pd
# df_mobile_val = pd.read_csv('./data/mobile_data_info_train_competition.csv')
# cl = df_mobile_val["Phone Model"].dropna().unique().astype(int)


#Three steps 
#
# 1.Generate HTML
# from htmldownloader.Ebay.mobile.htmlGenerator import HTMLGenerator
# htmlGen = HTMLGenerator()
# htmlGen.test1()

# 2.Run runner.py

# 3.outPut final csv
# from json2csv.json2csv import *
# final = Json2Csv()
# final.outputFinalCSV()


from json2csv.train_modifier import TrainModifier
trainModifier = TrainModifier()
trainModifier.modifyDataFrame()