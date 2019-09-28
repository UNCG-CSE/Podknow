import requests
import json
import sys
import csv
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
"id"
]
finalList = []
print(len(finalList))
for item in filteredResults:
    row = []
    for key,value in item.items():
        if key in headerList:
           row.append(value)
    finalList.append(row)
print(len(finalList))
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf8')
dataFrame = pd.DataFrame(finalList)
dataFrame.columns=headerList
print(dataFrame.head())
dataFrame.to_csv("top200Podcast.csv")