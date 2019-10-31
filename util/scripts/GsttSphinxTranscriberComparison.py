from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import os
import glob
import threading
import json
from pydub.utils import mediainfo
import time
import speech_recognition as sr
from pathlib import Path
import math
import librosa
import soundfile as sf
import wave

#http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/


# Loading google credentials.
credentialsFile = open(r"C:\Users\jwthrs\Projects\cs405\podknow\Podknow\credentials\jamie\setting.gcsettings")
credentials_ds = json.load(credentialsFile)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_ds["CREDENTIALS_PATH"]
podcastCloudStorage = credentials_ds["CLOUD_STORAGE_URI"]


client = speech_v1.SpeechClient()

podknowPath = str(Path().absolute().parent.parent)
# Assuming this tool is launched from inside /util/scripts
podcastNames = glob.glob(podknowPath + "/data/audio/*.flac")
podcastTranscriptOutputPath_gstt = podknowPath + "/data/transcripts/gcsst/raw/"
podcastTranscriptOutputPath_sphinx = podknowPath + "/data/transcripts/sphinx/raw/"

print("hello am i working")
for podcast in podcastNames:
    print(podcast)

language_code = "en-US"

encoding = enums.RecognitionConfig.AudioEncoding.FLAC

def scrubPathFromAudioFilePath(audiofile):
    return audiofile[audiofile.rindex('\\')+1:len(audiofile)]

def audioFileNameToTextOutPath(audioFileName, transcriptPath):
    return transcriptPath + scrubPathFromAudioFilePath(audioFileName[0:min(12, audioFileName.rindex('.'))])

# Sphinx transcription
def sphinxTranscribe(textOutput, podcastAudioPath):
    print("Sphinx transcribe called... for " + podcastAudioPath)
    rcgnr = sr.Recognizer()

    audioSource = sr.AudioFile(podcastAudioPath)

    audioDuration = int(math.floor(float(mediainfo(podcastAudioPath)['duration'])))
    audioStepTime = 60000 # 1 minutes.
    podSteps =  int(math.floor(audioDuration / audioStepTime))
    startTime = time.time()
    sampleRate = int(mediainfo(podcastAudioPath)['sample_rate'])

    with sr.AudioFile(audioSource) as tsource:
        for podStep in range(0, podSteps):
            audio = rcgnr.record(tsource, duration=audioStepTime)
            print("Iteration: " + str(podStep))
            try:
                print("Sphinx trying to transcribe...")
                transcription = rcgnr.recognize_sphinx(audio)
                f = open(textOutput, "a+")
                f.write(transcription)
                f.close()
            except sr.UnknownValueError:
                print("Sphinx couldn't interpret the audio")
            except sr.RequestError as e:
                print("ERROR: Sphinx: {0}".format(e))
    
    endTime = time.time()
    duration = endTime - startTime

    fstats = open(textOutput+"_stats.txt", "w")
    fstats.write("Transcription Time: " + str(duration))
    fstats.write("\nTranscription Method: Google Cloud Speech To Text")
    fstats.close()

    print("Sphinx finished transcribing!")

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
        f = open(textOutput+".txt", "a+")
        f.write((u"{}".format(alternative.transcript)))
        f.close()
    
    endTime = time.time()
    duration = endTime - startTime

    fstats = open(textOutput+"_stats.txt", "a+")
    fstats.write("Transcription Time: " + str(duration))
    fstats.write("Transcription Method: Google Cloud Speech To Text")

    print("Finished in: " + str(duration))

for audiofile in podcastNames:
    sampleRate = int(mediainfo(audiofile)['sample_rate'])
    print("File SR: " + str(sampleRate) + ", " + scrubPathFromAudioFilePath(audiofile))
    audio = {"uri": podcastCloudStorage+scrubPathFromAudioFilePath(audiofile)}
    #textOutputGstt = audioFileNameToTextOutPath(audiofile, podcastTranscriptOutputPath_gstt)
    #googleTranscribeThread = threading.Thread(target=transcribeFileInBucket, args=(audio, textOutput, sampleRate))
    #googleTranscribeThread.start()

    textOutputSphinx = audioFileNameToTextOutPath(audiofile, podcastTranscriptOutputPath_sphinx)
    sphinxTranscribe(textOutputSphinx, audiofile)



