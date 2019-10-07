import requests
import json
import sys
import csv
import pandas as pd
response = requests.get("https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/200/explicit.json")
jsonObject = response.content
print(jsonObject)
feed = {}
try:
    feed = json.loads(jsonObject)
    print(type(feed))
    for item, value in feed.items():
        print(item)
        print(value)
except (ValueError, KeyError, TypeError):
    print("Json Format Error")
feed = feed['feed']
results = feed['results']
filteredResults = []
for item in results:
    if "contentAdvisoryRating" in item.keys():
        del item["contentAdvisoryRating"]
    filteredResults.append(item)
headerList = ["kind",
"name",
"url",
"releaseDate",
"artistName",
"genres",
"id",
"user"
]

users = ["Jamie","Vincent","Chris","Jeremy","Harini"]

finalList = []

for item in filteredResults:
    row = []
    for key,value in item.items():
        if key in headerList:
            row.append(value)
    finalList.append(row)

print(len(finalList))

remaining=len(finalList)%len(users)

print(remaining)

eachUserList = int(len(finalList)/len(users))

print(eachUserList)

lastList = []


for user in users:
    for j in range(eachUserList):
        item = finalList[0]
        print(user)
        item.append(user)
        print(item)
        lastList.append(item)
        del finalList[0]

for i in range(len(finalList)):
    item = finalList[i]
    item.append(users[i])
    lastList.append(item)

dataframe = pd.DataFrame(lastList)

print(dataframe.head())

dataframe.to_csv("top200Podcast.csv")