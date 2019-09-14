from urllib.request import urlopen as uRequest
from urllib.request import urlretrieve as downloadFromUrl
from bs4 import BeautifulSoup as soup
from os import path
import pandas as pd
import time
from re import sub
import sys
import requests

baseUrl = "https://podbay.fm/podcast/"

def scrubFileOutputString(fileOutput):
    # Source: https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    fileOutput = sub('[^\w\s-]', '', fileOutput)
    return sub('[-\s]+', '',fileOutput)

def getExtension(url):
    if ".mp3" in url:
        return ".mp3"
    elif ".wav" in url:
        return ".wav"
    elif ".ogg" in url:
        return ".ogg"

def downloadRawHtml(url):
    webClient = uRequest(url)
    page_rawhtml = webClient.read()
    webClient.close()
    return page_rawhtml

def writeDownloadErrorText(errorStr):
    errorTxtFile = open("../../../data/audio/DownloadErrors.txt", "a+")
    errorTxtFile.write(errorStr)

#DON'T USE - downloadFromUrl reports invalid argument when using this method. Go figure??
def attemptDownloadAudioFromUrl(audioUrl, downloadPath):
    wasRedirect = False
    try:
        # Attempt to get redirect url.
        response = requests.get(str(audioUrl))
        if response.history:
            wasRedirect = True
            print("Original url was redirected to " + str(response.url))
            downloadFromUrl(str(response.url), downloadPath)
        else:
            downloadFromUrl(str(audioUrl), downloadPath)
        print("Successful!")
    except Exception as error:
        print("Failed! See error log.")
        errorStr = "ERROR: On attempting to download from " + audioUrl + ", error is as follows\n" + str(error) + "\nWas Redirect? : " + str(wasRedirect) + "\n\n"
        writeDownloadErrorText(errorStr)

def downloadLatestPodcastFromId(id, destPath):
    print("Downloading " + str(id) + " to " +  destPath)
    page_rawhtml = downloadRawHtml(baseUrl+str(id))


    # TODO: Check output of soup funcs to see if they fit expected format. If not then raise exceptions.
    # Put the html in my soup.
    page_soup = soup(page_rawhtml, "html.parser")

    # Grab relevant data: podcastname, date, episode title
    podcastName = page_soup.find("div", {"class":"main-meta"}).find("div",{"class":"meta"}).a.h1.text
    episodelist_soup = page_soup.find("div", {"class":"episode-list"})
    latestEpisode = episodelist_soup.div.div
    latestEpisodeMeta = latestEpisode.find("div", {"class":"meta"})

    # When we get trending episodes, we will want to match trending episodes with this variable.
    latestEpisodeDate = latestEpisodeMeta.find("div", {"class":"date"}).text
    latestEpisodeTitle = latestEpisodeMeta.find("div",{"class":"title"}).div.a.text

    # TODO: This url can get junk added to it which needs to be scrubbed. 
    # Errors out program when it encounters '?=...' b/c it will attempt to make it as a file name.
    latestEpisodeAudioUrl = latestEpisode.find("div", {"class":"download"}).a['href']

    # Prep paths for downloading.
    fileDownloadName = str(id)+"_"+podcastName+"_"+latestEpisodeDate+"_"+latestEpisodeTitle
    fileDownloadName = scrubFileOutputString(fileDownloadName) + getExtension(latestEpisodeAudioUrl)
    fullDownloadPath = destPath+fileDownloadName

    if path.exists(fullDownloadPath):
        print("The latest podcast is already downloaded!")
    else:
        print("To be named: " + fileDownloadName)
        print("From: " + latestEpisodeAudioUrl)
        response = requests.get(latestEpisodeAudioUrl)
        wasRedirect = False
        try:
            if response.history:
                wasRedirect = True
            downloadFromUrl(str(response.url), fullDownloadPath)
            print("Successful!")
        except Exception as error:
            print("Failed! See error log.")
            errorStr = "ERROR: On attempting to download " + str(id) + " from " + response.url + ", error is as follows\n" + str(error) + "\nWas Redirect? : " + str(wasRedirect) + "\n\n"
            writeDownloadErrorText(errorStr)

def interface():
    print("\n\tPodbay Webscraper\n\n")

    # TODO: Scrub & error check all input.
    csvPath = "../../../data/top200Podcast.csv"
    csvFileDF = pd.read_csv(csvPath)
    name = input("Enter your name: ")
    # TODO: Update gitignore to ignore all .mp3 files in audio path.
    destPath = "../../../data/audio/"

    userRows = csvFileDF[csvFileDF['user'].str.match(name)]
    idsToDownload = userRows['id'].tolist()
    for id in idsToDownload:
        downloadLatestPodcastFromId(id, destPath)
        time.sleep(1.5)

interface()

# TODO: Allow to be called with args 'Name'.
# TODO: Optimize downloads with multiple threads, 2 to 3 a time?
# TODO: Can we control throttle DL speed too?
# TODO: Handle HTTP Errors! Skip over if error, print error to .txt file