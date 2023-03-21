import pandas as pd
df = pd.read_csv("dataset.csv")
df.replace("Telangana ","Telangana", inplace = True)
df.replace("Tamilnadu ","Tamilnadu", inplace = True)
statelist = df["State"].tolist()
statelist = list(set(statelist))
statetocity = {}
for i in range(len(statelist)):
    for j in range(len(df["City"])):
        if statelist[i] == df.iloc[j]["State"]:
            if statelist[i] not in statetocity:
                statetocity[statelist[i]] = [df.iloc[j]["City"]]
            else:
                statetocity[statelist[i]].append(df.iloc[j]["City"])
for i in statetocity:
    statetocity[i] = list(set(statetocity[i]))
    print(i)
    print(statetocity[i])
    for j in range(len(df["Name"])):
        if citylist[i] == df.iloc[j]["City"]:
            if citylist[i] not in citytoplace:
                citytoplace[citylist[i]] = [df.iloc[j]["Name"]]
            else:
                citytoplace[citylist[i]].append(df.iloc[j]["Name"])
for i in citytoplace:
    citytoplace[i] = list(set(citytoplace[i]))
    print(i)
    print(citytoplace[i])


citylist = df["City"].tolist()
citylist = list(set(citylist))
citytoplace = {}
for i in range(len(citylist)):