
accLabels =  ["Brand","Network Technology", "Model", "Processor","Style","Storage Capacity","Manufacturer Color"
    "Color","Memory Card Type", "Network","Camera Resolution","Screen Size"]

clean = "Network Technology"
if (clean.upper() in (name.upper() for name in accLabels)):
    print("yes")
else:
    print("no")