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
from google.cloud import speech
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
print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
print(credentials_ds)


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
import subprocess

def splitToMonoFlac(targetName, srcFile):

    startTime = getCurrTime()

    targetPathStereo = audioPath+targetName.split('.')[0]+"_notmono.flac"
    targetPathMono = audioPath+targetName.split('.')[0]+".flac"

    if not os.path.exists(targetPathMono):
        length = float(mediainfo(srcFile)['duration'])
        subprocess.call(['ffmpeg', '-i', srcFile, targetPathStereo])
        subprocess.call(['ffmpeg', '-i', targetPathStereo, '-map_channel', '0.0.0', targetPathMono])
        newFileSize = os.path.getsize(targetPathMono.split('.')[0]+".flac")
        sampleRate = int(mediainfo(targetPathMono.split('.')[0]+".flac")['sample_rate'])
        os.remove(targetPathStereo)
        convDuration = getTimeElapsed(startTime)
        print("Duration: " + convDuration)
    else:
        length = float(mediainfo(srcFile)['duration'])
        sampleRate = int(mediainfo(targetPathMono.split('.')[0]+".flac")['sample_rate'])
        newFileSize = os.path.getsize(targetPathMono.split('.')[0]+".flac")
        convDuration = getTimeElapsed(startTime)

    return [targetName.split('.')[0]+".flac", convDuration, sampleRate, length, newFileSize]

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
    # filename, 1/0 for success, download duration in seconds, filesize
    ptinfo = [fileDownloadName, downloadSuccessful, 0, 0]

    if os.path.exists(fullDownloadPath):
        print("The latest podcast is already downloaded!")
    else:
        print("To be named: " + fileDownloadName)
        print("From: " + latestEpisodeAudioUrl)
        try:
            startTime = getCurrTime()
            response = requests.get(latestEpisodeAudioUrl)
            wasRedirect = False
            try:
                if response.history:
                    wasRedirect = True
                downloadFromUrl(str(response.url), fullDownloadPath)
                duration = getTimeElapsed(startTime)
                ptinfo[2] = duration
                ptinfo[3] = os.path.getsize(fullDownloadPath)
                print("Successful!")
            except Exception as error:
                print("Failed! See error log.")
                errorStr = "ERROR: On attempting to download " + str(id) + " from " + response.url + ", error is as follows\n" + str(error) + "\nWas Redirect? : " + str(wasRedirect) + "\n\n"
                downloadSuccessful = 0
                ptinfo[1] = downloadSuccessful
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
    pathToOutput = gcTranscriptPath + date + '\\'
    if not os.path.exists(pathToOutput):
        os.makedirs(gcTranscriptPath + date + '\\')
    ftrans = open(pathToOutput + outputName + "_output.txt", "w+")
    ftrans.write(str(stats))
    ftrans.flush()
    ftrans.close()


def transcriptResult(pStats, pTranscripts):
    return { 'Stats' : pStats, 'Transcripts' : pTranscripts}

# Statistics
def transcriptionStats(statsInput):
    '''
    0 => PodcastID
    1 => DownloadTime
    2 => AudioLength
    3 => OriginalFileSize
    4 => FlacFileSize
    5 => TranscriptionMethod
    6 => TranscriptionTime
    7 => DownloadSuccessful
    '''

    statsDict = {
        "PodcastID":statsInput[0],
        "DownloadTime":statsInput[1],
        "AudioLength":statsInput[2],
        "OriginalFileSize":statsInput[3],
        "FlacFileSize":statsInput[4],
        "TranscriptionMethod":statsInput[5],
        "TranscriptionTime":statsInput[6],
        "DownloadSuccessful":statsInput[7]
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
        print("uploading " + uploadFromFilePath + " to audiofiles/"+targetName)

        with open(uploadFromFilePath, 'rb') as pf:
            blob.upload_from_file(pf, num_retries=300)
            pf.flush()
            pf.close()
        
        duration = getTimeElapsed(startTime)
        print("Uploaded " + targetName)
    except Exception as e:
        print("Ran into error when attempting to establish the google cloud bucket client.")
        print(e)
        input("Upload this file manually then enter something to continue. ")
        input("Are you sure this file is uploaded?")
        input("Alrighty one more time then")

def googleCloudTranscribeFile(name, rawSampleRate, pStats):

    print("TRANSCRIBE FILE: " + audioPath+name)
    localAudioPath = audioPath+name
    print("Local audio path: " + localAudioPath)
    gcUploadUri = {"uri" : podcastCloudStorage + name}

    encoding = enums.RecognitionConfig.AudioEncoding.FLAC

    config = {
        "sample_rate_hertz" : rawSampleRate,
        "language_code" : "en-US",
        "encoding": encoding,
    }

    startTime = time.time()
    print(u"Transcribing... " + gcUploadUri['uri'])

    print(config)
    print(gcUploadUri)

    operation = client.long_running_recognize(config, gcUploadUri)

    print("Done transcribing, printing result:")

    response = operation.result()
    pTranscripts = []

    for result in response.results:
        firstAlternative = result.alternatives[0]
        transcript = u"{}".format(firstAlternative.transcript)
        confScore = firstAlternative.confidence
        pTranscript = [confScore, transcript]
        pTranscripts.append(pTranscript)

    endTime = time.time()
    duration = endTime - startTime
    pStats['TranscriptionTime'] = duration

    results = transcriptResult(pStats, pTranscripts)
    today = str(date.today())
    transcriptionOutput(today, name, results)

    print("Transcription for " + name + " has finished and took " + str(duration))

def googleCloudProcess(podcastName):
    # Converts the file to FLAC
    flacDestPath = audioPath + podcastName

    pinfo = splitToMonoFlac(podcastName, flacDestPath)

    flacResPath = audioPath + pinfo[0]

    googleCloudUploadFile(flacResPath, pinfo[0])
    return pinfo


def collectProcess(transcribeMethod):

    csvPath = "../../data/top200Podcast.csv"
    csvFileDF = pd.read_csv(csvPath)

    idsToDownload = csvFileDF['id'].tolist()

    if transcribeMethod == "googlecloud":
        for id in idsToDownload:

            today = str(date.today())
            transcriptionPath = gcTranscriptPath + today + '\\' + str(id)+".flac_output.txt"
            if os.path.exists(transcriptionPath):
                print("The transcription exists, skipping...")
                continue
            # Download
            print("Downloading " + str(id))
            ptinfo = downloadLatestPodcastFromId(id, audioPath)

            '''
            if ptinfo[1] == 0:
                # TODO: Write out file
                continue
            '''
            # Convert the podcast to a .flac, then upload the podcast to the gc bucket.
            print("Processing, converting to flac and uploading...")
            pinfo = googleCloudProcess(ptinfo[0])

            pStatsList = [ptinfo[0], ptinfo[1], pinfo[3], ptinfo[3], pinfo[4], "googlecloud", 0, ptinfo[2]]
            pStatsDict = transcriptionStats(pStatsList)

            # Tell google to start speech recog on a thread to allow more downloads
            print("Transcribing...")
            #googleCloudTranscribeFile(pinfo[0], pinfo[2], pStatsDict)
            transcribeThread = threading.Thread(target=googleCloudTranscribeFile, args=(pinfo[0], pinfo[2], pStatsDict))
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
