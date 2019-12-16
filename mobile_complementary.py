from mobile_api.fonoapi.fonoapi import FonoAPI
import json
import pandas as pd

API_TOKEN = '67c6b1f0f74d8feddc38f44481cc2b85c3374b3ec8fb051d'
fon  = FonoAPI(API_TOKEN)

attribute_list = ['DeviceName', 'Brand', 'technology', 'dimensions', 'size', 'resolution',
                  'camera_c', 'features_c', 'internal', 'netword_c', 'features',
                  'camera', 'display','_2g_bands', '_3g_bands', '_4g_bands', 'os',
                  'body_c', 'colors', 'primary_', 'multitouch', 'gps']

with open('./data/mobile_profile_train.json') as f:
    mobile_json = json.load(f)

# devices = mobile_json['Phone Model'].keys()
#
# devices_dict = {}
#
# for device in devices:
#     phones = fon.getdevice(device)
#     phones_df = phones.dataframe(attribute_list)
#     devices_dict[device] = phones_df
#
# devices_dict_clean = {k: v for k, v in devices_dict.items() if (v.shape[0] >=1)}
#
# for key, value in devices_dict_clean.items():
#     print(key)
#     value = value[value['DeviceName'].str.lower() == key]
#     devices_dict_clean[key] = value
#
# devices_dict_clean_2 = {k: v for k, v in devices_dict_clean.items() if (v.shape[0] >=1)}
# mobile_df = pd.DataFrame(columns = attribute_list)
#
# for key, value in devices_dict_clean_2.items():
#     mobile_df = mobile_df.append(value)

color_list = ['blue', 'biru',
              'gold', 'emas',
              'brown', 'coklat',
              'navy blue', 'biru laut',
              'yellow', 'kuning',
              'neutral', 'netral',
              'rose gold', 'mawar emas',
              'light blue', 'biru muda',
              'dark grey', 'Abu-abu gelap',
              'silver', 'perak',
              'pink', 'berwarna merah muda',
              'gray', 'abu-abu',
              'army green','hijau tentara',
              'deep blue', 'biru tua',
              'purple', 'ungu',
              'rose', 'mawar',
              'light grey', 'Abu-abu terang',
              'deep black', 'hitam pekat',
              'off white', 'putih pucat',
              'multicolor', 'beraneka warna',
              'black', 'hitam',
              'apricot', 'aprikot',
              'orange', 'jeruk',
              'green', 'hijau',
              'white', 'putih',
              'red', 'merah'
              ]

