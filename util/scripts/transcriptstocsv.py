from pathlib import Path
import json
import os

rootPath = str(Path().absolute().parent.parent)
transcriptsPath = "\\data\\transcripts\\gcstt\\raw\\2019-10-30\\"

jsonFilesPath = rootPath + transcriptsPath

alljsonfiles = os.listdir(jsonFilesPath)

djsonFiles = []

for dfile in range(len(alljsonfiles)):
    try:
        with open(jsonFilesPath+alljsonfiles[dfile]) as pf:
            jsonFile = json.load(pf)
            djsonFiles.append(jsonFile)
    except Exception as e:
        print(e)

jsonFileCount = len(djsonFiles)

import pandas as pd 

# I want PodcastID, the AudioFileLength, and a list of confidence scores for each podcast.

df = pd.DataFrame(columns=["PodcastID", "AudioLength","ConfidenceScores","OverallConfidence"])

jsonFileCount = len(djsonFiles)

pdf_conf = pd.DataFrame(columns=["ConfScore", "WordCount"])

for jsfEntry in djsonFiles:
    
    pdf_temp = pd.DataFrame(columns=["ConfScore","WordCount"])
    
    for n in range(len(jsfEntry['Transcripts'])):
        wordCount = 1
        for i in str(jsfEntry['Transcripts'][n][1]):
            if (i==' '):
                wordCount = wordCount + 1
        pdf_temp.loc[i] = [jsfEntry['Transcripts'][n][0]] + [ wordCount ]
    
    pdf_conf = pdf_conf.append(pdf_temp)

pdf_conf.reset_index()
print(pdf_conf.head(10))
pdf_conf.plot(kind="scatter", x="ConfScore", y="WordCount", figsize=(10,8))

pdf_conf.to_csv(rootPath + "\\data\\wc-cs.csv")




