from urllib.request import urlopen as uRequest
from urllib.request import urlretrieve as downloadFromUrl
from bs4 import BeautifulSoup as soup
from os import path
import pandas as pd
import time

baseUrl = "https://podbay.fm/podcast/"

def scrubFileOutputString(fileOutput):
    return fileOutput.replace(" ", "").replace(",", "").replace("?","")

def getExtension(url):
    return url[url.rindex('.'):len(url)]

def downloadRawHtml(url):
    webClient = uRequest(url)
    page_rawhtml = webClient.read()
    webClient.close()
    return page_rawhtml

def downloadLatestPodcastFromId(id, destPath):
    print("Downloading " + str(id) + " to " +  destPath)
    page_rawhtml = downloadRawHtml(baseUrl+str(id))

    # Parse html with soup.
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
        downloadFromUrl(latestEpisodeAudioUrl, fullDownloadPath)

    print(fileDownloadName)
    print(latestEpisodeAudioUrl)

def interface():
    print("\n\tPodbay Webscraper\n\n")

    # TODO: Scrub & error check all input.
    csvPath = input("Enter trending csv path: ")
    csvFileDF = pd.read_csv(csvPath)
    name = input("Enter your name: ")
    destPath = input("Enter download destination path: ")

    userRows = csvFileDF[csvFileDF['user'].str.match(name)]
    idsToDownload = userRows['id'].tolist()
    for id in idsToDownload:
        downloadLatestPodcastFromId(id, destPath)
        time.sleep(3)

interface()

# TODO: Allow to be called with args.