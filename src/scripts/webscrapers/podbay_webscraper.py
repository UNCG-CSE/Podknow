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

    page_soup = soup(page_rawhtml, "html.parser")
    podcastName = page_soup.find("div", {"class":"main-meta"}).find("div",{"class":"meta"}).a.h1.text
    episodelist_soup = page_soup.find("div", {"class":"episode-list"})
    latestEpisode = episodelist_soup.div.div
    latestEpisodeMeta = latestEpisode.find("div", {"class":"meta"})

    #Later on, when we get trending episodes, we will want to match trending episodes with this variable.
    latestEpisodeDate = latestEpisodeMeta.find("div", {"class":"date"}).text
    latestEpisodeTitle = latestEpisodeMeta.find("div",{"class":"title"}).div.a.text
    latestEpisodeAudioUrl = latestEpisode.find("div", {"class":"download"}).a['href']
    fileDownloadName = podcastName+"_"+latestEpisodeDate+"_"+latestEpisodeTitle
    fileDownloadName = scrubFileOutputString(fileDownloadName) + getExtension(latestEpisodeAudioUrl)
    fullDownloadPath = destPath+fileDownloadName

    if path.exists(fullDownloadPath):
        print("The latest podcast is already downloaded!")
    else:
        downloadFromUrl(latestEpisodeAudioUrl, fullDownloadPath)

    print(fileDownloadName)
    print(latestEpisodeAudioUrl)


def interface():
    print("\tPodbay Webscraper\n\n")
    #Set Trending csv path.
    csvPath = input("Enter trending csv path: ")
    csvFileDF = pd.read_csv(csvPath)

    #Set name.
    name = input("Enter your name: ")
    #Set download path.
    destPath = input("Enter download destination path: ")


    userRows = csvFileDF[csvFileDF['user'].str.match(name)]
    idsToDownload = userRows['id'].tolist()
    for id in idsToDownload:
        downloadLatestPodcastFromId(id, destPath)
        time.sleep(3)
    #Get all podcast IDs associated with name from csv.
    #Download each from each podcast ID.
    #Exit

interface()
#
#itunesID = "1458568923"
#Please give the of your Podknow repository. The path should have the src, util, and data folders as direct children.
#destPathPodknowRepo = "C:\\Users\\jwthrs\\Projects\\cs405\\podknow\\Podknow\\"
#Audio will be stored in data\audio\
#destPathDataAudio = "data\\audio\\"
#fullDestPath = destPathPodknowRepo + destPathDataAudio

#downloadLatestPodcastFromId(itunesID, fullDestPath)

#Create folder for podcast if it doesnt exist.
#Download file to that path.


#Need class that has "episode-list" in its name.
#Get the div inside of it.
#Get the first div inside of above div.
#Get class that has "download" in its name
#Get the .mp3 href.