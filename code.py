import pandas as pd
import requests
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

# for i in state_city:
#     print(i,state_city[i])
#
# print('-------------------------------------------')
#
# for i in city_place:
#     print(i,city_place[i])

locpoints= ["77.983936,28.255904","77.05993,28.487555","77.15993,28.587555","77.25993,28.687555"]
p1 = "https://apis.mapmyindia.com/advancedmaps/v1/2dfdb55d-3f12-4739-bdc5-2d85c76fcd57/distance_matrix/driving/"
p2 = "?sources="
p3 = "&destinations="
for i in range(len(locpoints)):
    if i == len(locpoints)-1:
        p1 = p1+locpoints[i]
        p2 = p2 + str(i)
        p3 = p3 + str(i)
    else:
        p1 = p1+locpoints[i]+";"
        p2 = p2 + str(i) + ";"
        p3 = p3 + str(i) + ";"

response = requests.get(p1+p2+p3, headers={'Authorization': '2dfdb55d-3f12-4739-bdc5-2d85c76fcd57'})
d = response.json()
dismat = []
durmat = []
for i in d['results']['distances']:
    dismat.append(i)
for i in d['results']['durations']:
    durmat.append(i)
print(dismat)
print(durmat)


