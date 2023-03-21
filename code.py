import pandas as pd
df = pd.read_csv('dataset.csv')

print(df.columns.values)
print(df.shape[0])

state_city = {}
city_place = {}

statelist = df["State"].tolist()
statelist = list(set(statelist))

citylist = df["City"].tolist()
citylist = list(set(citylist))

for i in range(0,df.shape[0]):
    if df.iloc[i]['State'] not in state_city.keys():
        state_city[df.iloc[i]['State']] = [df.iloc[i]['City']]
    elif df.iloc[i]['State'] in state_city.keys() and df.iloc[i]['City'] not in state_city[df.iloc[i]['State']]:
        state_city[df.iloc[i]['State']].append(df.iloc[i]['City'])

for i in range(0,df.shape[0]):
    if df.iloc[i]['City'] not in city_place.keys():
        city_place[df.iloc[i]['City']] = [df.iloc[i]['Name']]
    elif df.iloc[i]['City'] in city_place.keys() and df.iloc[i]['Name'] not in city_place[df.iloc[i]['City']]:
        city_place[df.iloc[i]['City']].append(df.iloc[i]['Name'])

for i in state_city:
    print(i,state_city[i])

print( '-------------------------------------------')

for i in city_place:
    print(i,city_place[i])
