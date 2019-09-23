from google.cloud import speech
from google.cloud.speech import types
from google.cloud.speech import enums
import time
import threading
import io 
import os
import glob
from pydub.utils import mediainfo


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\Users\\vince\Desktop\\MyGoogleCloudService\\linear-equator-253121-2b458fe691e7.json"

client = speech.SpeechClient()

podcastNames = glob.glob("../../data/audio/*.flac")

podcastTranscriptOutputPath = "../../data/transcripts/gcsst/raw/"

podcastCloudStorage = 'gs://datasciencepodknow/audios/'

print(podcastNames)

language_code = "en-US"

encoding = enums.RecognitionConfig.AudioEncoding.FLAC

def scrubPathFromAudioFilePath(audiofile):
    return audiofile[audiofile.rindex('\\')+1:len(audiofile)]

def audioFileNameToTextOutPath(audioFileName):
    return podcastTranscriptOutputPath + scrubPathFromAudioFilePath(audioFileName[0:audioFileName.rindex('.')+1] + "txt")

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
    transcribeThread = threading.Thread(target=transcribeFileInBucket, args=(audio, textOutput, sampleRate))
    transcribeThread.start()
