from os import path
import pandas as pd
import time
from re import sub
import sys
import requests

# Streamlined version of the full app as it was overdesigned.



# Split audio files to mono if not mono
from glob import glob
from pydub import AudioSegment

def splitToMono(audioPath, name, srcFile):
    podcastAudio = AudioSegment.from_file(srcFile)
    ptracks = podcastAudio.split_to_mono()
    newpAudio = ptracks[0].set_channels(1)
    newpAudio.export(audioPath+name, format="flac")

# Podbay download
from urllib.request import urlopen as uRequest
from urllib.request import urlretrieve as downloadFromUrl
from bs4 import BeautifulSoup as soup

def scrubFileOutputString(fileOutput):
    # Source: https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    fileOutput = sub(r'[^\w\s-]', '', fileOutput)
    fileOutput = sub(r'[-\s]+', '',fileOutput)
    # Cut off after 12 characters.
    fileOutput = fileOutput[0:min(12, len(fileOutput))]
    return fileOutput

def getExtension(url):
    if ".mp3" in url:
        return ".mp3"
    elif ".wav" in url:
        return ".wav"
    elif ".ogg" in url:
        return ".ogg"
    elif ".m4a" in url:
        return ".m4a"

def downloadRawHtml(url):
    webClient = uRequest(url)
    page_rawhtml = webClient.read()
    webClient.close()
    return page_rawhtml

def writeDownloadErrorText(errorStr):
    errorTxtFile = open("../../../data/audio/DownloadErrors.txt", "a+")
    errorTxtFile.write(errorStr)

def downloadLatestPodcastFromId(id, destPath):
    baseUrl = "https://podbay.fm/podcast/"
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
        try:
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
        except Exception as err1:
            errorStr = "Could not reach url " + latestEpisodeAudioUrl
            print(errorStr)
            writeDownloadErrorText(errorStr)

# Transcription methods

# Output

def transcriptionOutput(date, name, stats, transcript):
    outputName = str(date) + "/" + str(name)

    fstats = open(outputName+"_stats.txt", "a+")
    fstats.write(stats)
    fstats.close()

    ftrans = open(outputName+"_transcript.txt", "a+")
    ftrans.write(transcript)
    ftrans.close()

    print("Not implemented.")

# Statistics
def transcriptionStats():
    print("Not implemented.")

def getCurrTime():
    return time.time()

def getTimeElapsed(startTime):
    endTime = getCurrTime()
    return str(endTime - startTime)

from pocketsphinx import AudioFile
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

def psphinxTranscribeFile(audioPath):
    audio = AudioFile()
    model_path = get_model_path()
    
    config = {
        'verbose': False,

    }

    # May be a bit much to open a bunch of audio files ourselves to transcribe. 5 max?
    print("Not implemented.")

def psphinxProcessor():
    print("Not implemented.")

# Upload flac files to google cloud, then transcribe when ready.

currentlyUploading = 0

def googleCloudUploadFile():
    print("Not implemented.")

def googleCloudTranscribeFile():
    print("Not implemented.")

def googleCloudProcessor():
    # Uploads up to 3 at a time
    # Start transcribing as soon as finished uploading.
    print("Not implemented.")

# Check if cli args valid
def validateArguments(argsv):
    print("Not implemented.")

# Collector main
def collect():
    print(get_data_path())
    print("Not implemented.")

collect()
