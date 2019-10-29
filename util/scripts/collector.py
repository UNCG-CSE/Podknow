import os
import pandas as pd
import time
from re import sub
import sys
import requests
from pathlib import Path
import threading
import json
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

# Streamlined version of the full app as it was overdesigned.

# Audio path
rootPath = podknowPath = str(Path().absolute().parent.parent)
audioPath = rootPath + "\\data\\audio\\"
sphinxTranscriptPath = rootPath + "\\data\\transcripts\\sphinx\\raw\\"
gcTranscriptPath = rootPath + "\\data\\transcripts\\gcstt\\raw\\"

credentialsFile = open(r"C:\Users\jwthrs\Projects\cs405\podknow\Podknow\credentials\jamie\setting.gcsettings")
credentials_ds = json.load(credentialsFile)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_ds["CREDENTIALS_PATH"]
podcastCloudStorage = credentials_ds["CLOUD_STORAGE_URI"]


client = speech_v1.SpeechClient()

podknowPath = str(Path().absolute().parent.parent)
# Assuming this tool is launched from inside /util/scripts
podcastTranscriptOutputPath_gstt = podknowPath + "/data/transcripts/gcsst/raw/"
podcastTranscriptOutputPath_sphinx = podknowPath + "/data/transcripts/sphinx/raw/"

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
    fileDownloadName = fileDownloadName[0:min(12, len(fileDownloadName))]
    fileDownloadName = scrubFileOutputString(fileDownloadName) + getExtension(latestEpisodeAudioUrl)
    fullDownloadPath = destPath+fileDownloadName + getExtension(latestEpisodeAudioUrl)

    # Cut off after 12 characters.

    if Path.exists(fullDownloadPath):
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
    return fileDownloadName

# Transcription methods

# Output

def transcriptionOutput(date, name, stats, transcript):
    outputName = str(name)

    fstats = open(sphinxTranscriptPath+outputName+"_stats.txt", "a+")
    fstats.write(stats)
    fstats.close()

    ftrans = open(sphinxTranscriptPath+outputName+"_transcript.txt", "a+")
    ftrans.write(transcript)
    ftrans.close()

    print("Not implemented.")

# Statistics
def transcriptionStats(statsInput):
    statsDict = {
        "TranscriptionMethod":statsInput[0],
        "TranscriptionTime":statsInput[1],
        "OverallConfidence":statsInput[2]
    }
    return statsDict

def getCurrTime():
    return time.time()

def getTimeElapsed(startTime):
    endTime = getCurrTime()
    return str(endTime - startTime)

import pocketsphinx as ps
from pocketsphinx import AudioFile
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

def psphinxTranscribeFile(podcastFileName):
    model_path = get_model_path()
    
    hmm = os.path.join(model_path, 'en-us')
    lm = os.path.join(model_path, 'en-us.lm.bin')
    psdict = os.path.join(model_path, 'cmudict-en-us.dict')
    audioFile = audioPath + podcastFileName

    config = {
        'hmm': os.path.join(model_path, 'en-us'),
        'lm': os.path.join(model_path, 'en-us.lm.bin'),
        'dict': os.path.join(model_path, 'cmudict-en-us.dict')
    }

    startTime = getCurrTime()
    print("Transcribing... " + audioPath+podcastFileName)

    speechRec = Pocketsphinx(**config)

    speechRec.decode(
        audio_file=audioFile,
        buffer_size=2048,
        no_search=False,
        full_utt=False
    )

    transcriptionStr = speechRec.hypothesis()

    timeElapsed = getTimeElapsed(startTime)

    confScore = speechRec.confidence()

    statsInput = ["Sphinx",timeElapsed, confScore]

    statsDict = str(transcriptionStats(statsInput))

    transcriptionOutput("", podcastFileName, statsDict, transcriptionStr)

    # May be a bit much to open a bunch of audio files ourselves to transcribe. 5 max?
def psphinxProcess():
    # Converts file to RAW
    print("Not implemented.")

# Upload flac files to google cloud, then transcribe when ready.

currentlyUploading = 0

def googleCloudUploadFile():
    print("Not implemented.")

def googleCloudTranscribeFile():
    print("Not implemented.")

def googleCloudProcess(podcastName):
    # Converts the file to FLAC
    # Uploads 1 at a time
    # Start transcribing as soon as finished uploading.
    print("Not implemented.")

def collectProcess(transcriptMethod):

    csvPath = "../../data/top200Podcast.csv"
    csvFileDF = pd.read_csv(csvPath)


    idsToDownload = csvFileDF['id'].tolist()

    if transcriptMethod == "gc":
        for id in idsToDownload:
            # Download
            podcastName = downloadLatestPodcastFromId(id, audioPath)
            transcribeThread = threading.Thread(target=googleCloudProcess, args=(id))
            googleCloudProcess(podcastName)
    elif transcriptMethod == "sphinx":
        for id in idsToDownload:
            podcastName = downloadLatestPodcastFromId(id, audioPath)

    else:
        print("You dun goofed son.")
        exit()
            

# Check if cli args valid
def validateArguments(argsv):
    print("Not implemented.")

# Collector main
def collect():
    print(audioPath)
    psphinxTranscribeFile("welcometoresistance_sphinxVsgstt.flac")

collect()
