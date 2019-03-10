import json

# Define categories and category feature columns
categories = ['beauty', 'fashion', 'mobile']
category_feature_columns = {'beauty':[ 'Brand', 'Colour_group', 'Benefits', 'Product_texture', 'Skin_type'],
                   'fashion': ['Collar Type', 'Sleeves', 'Pattern', 'Fashion Trend', 'Clothing Material'],
                   'mobile': ['Operating System', 'Features',
       'Network Connections', 'Memory RAM', 'Brand', 'Warranty Period',
       'Storage Capacity', 'Color Family', 'Phone Model', 'Camera',
       'Phone Screen Size']}


### Open the json file

with open('./data/beauty_profile_train.json') as f:
    beauty_json = json.load(f)
with open('./data/fashion_profile_train.json') as f:
    fashion_json = json.load(f)
with open('./data/mobile_profile_train.json') as f:
    mobile_json = json.load(f)


category_json = {'beauty': beauty_json, 'fashion':fashion_json, 'mobile':mobile_json}