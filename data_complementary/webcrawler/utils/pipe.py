#Ebay key
EbayKey = ["Operating System","Features","Brand", "Warranty","Network Technology","Storage Capacity", 
"Color","RAM","Camera Resolution","Screen Size"]

#Shopee Key
ShopeeKey = ["Operating System","Features","Brand", "Warranty Period","Network Connections","Storage Capacity", 
"Color Family","Memory RAM","Camera","Phone Screen Size"]

def ebayJsonKeyPipe(ebayKey):
    return ShopeeKey[EbayKey.index(ebayKey)]


def isShopeeKeyArrayValue(shopeeKey):
    if shopeeKey == "Camera" or shopeeKey == "Color Family" or shopeeKey == "Storage Capacity":
        return True
    else:
        return False