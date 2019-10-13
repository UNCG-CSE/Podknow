import json
import sys
import csv
import requests
import pandas as pd


class iTunesPodcastRSS:
    def __init__(self, path):
        self.path = path
        self.headerList = ["kind",
        "name",
        "url",
        "releaseDate",
        "artistName",
        "id"
        ]

    def parseRequest(self):
        response = requests.get(self.path)
        jsonObject = response.content
        feed = {}
        try:
            feed = json.loads(jsonObject)
            for key, value in feed.items():
                print(key)
                print(value)
        except (ValueError, KeyError, TypeError) as e:
            print(e)
        newFeed = feed['feed']
        results = newFeed['results']
        filteredResults = []
        for item in results:
            if "contentAdvisoryRating" in item.keys():
                del item["contentAdvisoryRating"]
            filteredResults.append(item)
        finalList = []
        for item in filteredResults:
            row = []
            for key, value in item.items():
                if key in self.headerList:
                    row.append(value)
            finalList.append(row)
        import sys
        #reload(sys)
        #sys.setdefaultendcoding('utf8')
        dataFrame = pd.DataFrame(finalList)
        dataFrame.columns = self.headerList
        dataFrame.to_csv("top200Podcast.csv")
        