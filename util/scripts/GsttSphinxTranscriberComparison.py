from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import os
import glob
import threading
import json
from pydub.utils import mediainfo
import time
import speech_recognition as sr

#http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/


# Loading google credentials.
credentialsFile = open(r"C:\Users\jwthrs\Projects\cs405\podknow\Podknow\credentials\jamie\settings.gcsettings")
credentials_ds = json.load(credentialsFile)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_ds["CREDENTIALS_PATH"]
podcastCloudStorage = credentials_ds["CLOUD_STORAGE_URI"]


client = speech_v1.SpeechClient()

# Assuming this tool is launched from inside /src/util/scripts
podcastNames = glob.glob("../../../data/audio/*.flac")
podcastTranscriptOutputPath = "../../../data/transcripts/gcsst/raw/"




language_code = "en-US"

encoding = enums.RecognitionConfig.AudioEncoding.FLAC

def scrubPathFromAudioFilePath(audiofile):
    return audiofile[audiofile.rindex('\\')+1:len(audiofile)]

def audioFileNameToTextOutPath(audioFileName):
    return podcastTranscriptOutputPath + scrubPathFromAudioFilePath(audioFileName[0:min(12, audioFileName.rindex('.')+1)] + "txt")

# Sphinx transcription
def sphinxTranscribe(textOutput, podcastAudio):
    rcgnr = sr.Recognizer()
    with sr.AudioFile(podcastAudio) as tsource:
        audio = rcgnr.record(tsource)
    try:
        transcription = rcgnr.recognize_sphinx(audio)
        f = open(textOutput, "a+")
        f.write(transcription)
        f.close()
    except sr.UnknownValueError:
        print("Sphinx couldn't interpret the audio")
    except sr.RequestError as e:
        print("ERROR: Sphinx: {0}".format(e))


#Gcstt transcription
def transcribeFileInBucket(audioUriObject, textOutput, sampleRate):

    config = {
    "sample_rate_hertz": sampleRate,
    "language_code": language_code,
    "encoding": encoding,
    }

    startTime = time.time()
    operation = client.long_running_recognize(config, audioUriObject)
    print(u"Transcribing... " + audioUriObject['uri'])
    response = operation.result()

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"{}".format(alternative.transcript))
        f = open(textOutput, "a+")
        f.write((u"{}".format(alternative.transcript)))
        f.close()
    
    endTime = time.time()
    duration = endTime - startTime
    print("Finished in: " + str(duration))

for audiofile in podcastNames:
    sampleRate = int(mediainfo(audiofile)['sample_rate'])
    print("File SR: " + str(sampleRate) + ", " + scrubPathFromAudioFilePath(audiofile))
    audio = {"uri": podcastCloudStorage+scrubPathFromAudioFilePath(audiofile)}
    textOutput = audioFileNameToTextOutPath(audiofile)
    googleTranscribeThread = threading.Thread(target=transcribeFileInBucket, args=(audio, textOutput, sampleRate))
    googleTranscribeThread.start()

    sphinxTranscribeThread = threading.Thread(target=sphinxTranscribe, args=(textOutput, audiofile))
    sphinxTranscribeThread.start()



