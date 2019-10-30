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
from google.cloud import storage
from pydub.utils import mediainfo
from datetime import date

# Streamlined version of the full app as it was overdesigned.

# Audio path
rootPath = podknowPath = str(Path().absolute().parent.parent)
audioPath = rootPath + "\\data\\audio\\"
sphinxTranscriptPath = rootPath + "\\data\\transcripts\\sphinx\\raw\\"
gcTranscriptPath = rootPath + "\\data\\transcripts\\gcstt\\raw\\"

# Need second argument to select which user to get credentials from.
credentialsFile = open(r"C:\Users\jwthrs\Projects\cs405\podknow\Podknow\credentials\jamie\setting.gcsettings")
credentials_ds = json.load(credentialsFile)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_ds["CREDENTIALS_PATH"]
podcastCloudStorage = credentials_ds["CLOUD_STORAGE_URI"]
bucketName = credentials_ds["CLOUD_STORAGE_NAME"]


client = speech_v1.SpeechClient()

podknowPath = str(Path().absolute().parent.parent)
# Assuming this tool is launched from inside /util/scripts
podcastTranscriptOutputPath_gstt = podknowPath + "/data/transcripts/gcsst/raw/"
podcastTranscriptOutputPath_sphinx = podknowPath + "/data/transcripts/sphinx/raw/"

def getCurrTime():
    return time.time()

def getTimeElapsed(startTime):
    endTime = getCurrTime()
    return str(endTime - startTime)

# Split audio files to mono if not mono
from glob import glob
from pydub import AudioSegment

def splitToMonoFlac(targetName, srcFile):
    startTime = getCurrTime()
    podcastAudio = AudioSegment.from_file(srcFile)
    ptracks = podcastAudio.split_to_mono()
    newpAudio = ptracks[0].set_channels(1)
    newpAudio.export(audioPath+targetName.split('.')[0]+".flac", format="flac")
    print("Wrote new flac file to " + audioPath+targetName)
    duration = getTimeElapsed(startTime)
    
    import gc
    del podcastAudio
    gc.collect()

    return [targetName.split('.')[0]+".flac", duration]

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
    fileDownloadName = str(id) + getExtension(latestEpisodeAudioUrl)
    fullDownloadPath = destPath+fileDownloadName
    
    downloadSuccessful = 1
    ptinfo = [fileDownloadName, podcastName, latestEpisodeDate, latestEpisodeTitle, latestEpisodeAudioUrl, downloadSuccessful]

    if os.path.exists(fullDownloadPath):
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
                downloadSuccessful = 0
                ptinfo[5] = downloadSuccessful
                writeDownloadErrorText(errorStr)
        except Exception as err1:
            errorStr = "Could not reach url " + latestEpisodeAudioUrl
            print(errorStr)
            writeDownloadErrorText(errorStr)
    return ptinfo

# Transcription methods

# Output

def transcriptionOutput(date, name, stats):
    outputName = str(name)

    print("Stats: " + str(stats))
    ftrans = open(gcTranscriptPath + date + "\\" + outputName + "_output.txt", "a+")
    ftrans.write(stats)
    ftrans.close()

# Statistics
def transcriptionStats(statsInput):
    statsDict = {
        "DownloadTime":statsInput[0],
        "TranscriptionMethod":statsInput[1],
        "TranscriptionTime":statsInput[2],
        "OverallConfidence":statsInput[3],
        "Transcript": statsInput[4]
    }
    return statsDict


import pocketsphinx as ps
from pocketsphinx import AudioFile
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

def psphinxTranscribeFile(podcastFileName):
    '''
    model_path = get_model_path()
    podcastAudioFile = audioPath + podcastFileName
    
    config = {
        'hmm': os.path.join(model_path, 'en-us'),
        'lm': os.path.join(model_path, 'en-us.lm.bin'),
        'dict': os.path.join(model_path, 'cmudict-en-us.dict')
    }

    startTime = getCurrTime()
    print("Transcribing... " + audioPath+podcastFileName)

    speechRec = Pocketsphinx(**config)

    speechRec.decode(
        audio_file=podcastAudioFile,
        buffer_size=2048,
        no_search=False,
        full_utt=False)

    transcriptionStr = speechRec.hypothesis()

    timeElapsed = getTimeElapsed(startTime)

    confScore = speechRec.confidence()

    statsInput = ["Sphinx",timeElapsed, confScore]

    statsDict = str(transcriptionStats(statsInput))

    transcriptionOutput("", podcastFileName, statsDict, transcriptionStr)
    '''
    print("Broken.")

    # May be a bit much to open a bunch of audio files ourselves to transcribe. 5 max?
def psphinxProcess():
    # Converts file to RAW
    print("Not implemented.")

# Upload flac files to google cloud, then transcribe when ready.

def googleCloudUploadFile(uploadFromFilePath, targetName):
    
    storageClient = storage.Client()
    try:
        bucket = storageClient.get_bucket(bucketName)
        startTime = getCurrTime()
        blob = bucket.blob("audiofiles/"+targetName)

        with open(uploadFromFilePath, 'rb') as pf:
            blob.upload_from_file(pf)
            pf.close()
        
        duration = getTimeElapsed(startTime)
        print("Uploaded " + targetName)
    except Exception as e:
        print("Ran into error when attempting to establish the google cloud bucket client.")
        print(e)
    
def googleCloudTranscribeFile(name, duration):

    print("TRANSCRIBE FILE: " + audioPath+name)
    sampleRate = int(mediainfo(audioPath+name)['sample_rate'])
    gcUploadUri = {"uri" : podcastCloudStorage + name}
    config = {
        "sample_rate_hertz" : sampleRate,
        "language_code" : "en-US",
        "encoding": enums.RecognitionConfig.AudioEncoding.FLAC
    }

    startTime = time.time()
    print(u"Transcribing... " + gcUploadUri['uri'])
    operation = client.long_running_recognize(config, gcUploadUri)
    response = operation.result()

    for result in response.results:
        firstAlternative = result.alternatives[0]
        transcript = firstAlternative.transcript
        confScore = firstAlternative.confidence
        stats = [transcript, confScore, duration]
        today = str(date.today())
        transcriptionOutput(today, name, stats)
    
    endTime = time.time()
    duration = endTime - startTime

    print("Transcription for " + name + " has finished and took " + duration)

def googleCloudProcess(podcastName):
    # Converts the file to FLAC
    flacDestPath = audioPath + podcastName

    pinfo = splitToMonoFlac(podcastName, flacDestPath)

    googleCloudUploadFile(flacDestPath, pinfo[0])
    return pinfo

def collectProcess(transcribeMethod):

    csvPath = "../../data/top200Podcast.csv"
    csvFileDF = pd.read_csv(csvPath)

    idsToDownload = csvFileDF['id'].tolist()

    if transcribeMethod == "googlecloud":
        for id in idsToDownload:
            # Download
            print("Downloading " + str(id))
            ptinfo = downloadLatestPodcastFromId(id, audioPath)
            # Convert the podcast to a .flac, then upload the podcast to the gc bucket.
            print("Processing, converting to flac and uploading...")
            pinfo = googleCloudProcess(ptinfo[0])

            # Tell google to start speech recog on a thread to allow more downloads
            print("Transcribing...")
            transcribeThread = threading.Thread(target=googleCloudTranscribeFile, args=(pinfo[0], pinfo[1]))
            transcribeThread.start()

    elif transcribeMethod == "sphinx":
        for id in idsToDownload:
            podcastName = downloadLatestPodcastFromId(id, audioPath)
    elif transcribeMethod == "both":
        print("Not supported")
    else:
        print("You dun goofed son.")
        exit()
            

argList = ["googlecloud", "sphinx", "both"]
# Check if cli args valid
def validateArguments(argsv):
    return argsv.lower() in argList

# DEBUG: Exit if sphinx or both are entered.
def debugExit(argsv):
    arg = sys.argv[1].lower()
    if arg == "sphinx" or arg == "both":
        print("Not supported yet.")
        exit()

import sys
# Collector main
def collect():

    arg = sys.argv[1].lower()
    debugExit(arg)

    if not (validateArguments(sys.argv[1])):
        exit()
    
    collectProcess(arg)


collect()
