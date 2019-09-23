# TODO: SpeechToText.py will host a given audio file to Google cloud and then transcribe them to a provided path. It acquires Google Cloud Credentials from a local cloud json file.
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import os
import time
import glob
import json


CLOUDSETTINGS_CREDENTIALS = "CREDENTIALS_PATH"

CLOUDSETTINGS_CLOUD_STORAGE = "CLOUD_STORAGE_URI"

def fetchCloudSettings():
    """
    Finds the Google Cloud Settings file within the Podknow repository and returns a dictionary of the settings.        Returns None if path is incorrect.
    """
    # Assume first one is valid for now
    potentialPaths = glob.glob("../../../*.gcsettings")
    # TODO: Try all paths until one works.
    if len(potentialPaths) > 0:
        return getCloudSettingsFromFile(potentialPaths[0])
    else:
        raise Exception("File nowhere to be found in directory!")

def getCloudSettingsFromFile(path):
    parsedJson = json.loads(path)

    if parsedJson[CLOUDSETTINGS_CREDENTIALS] is None or parsedJson[CLOUDSETTINGS_CLOUD_STORAGE] is None:
        raise Exception("File found, but not populated with values!")
    else:
        return parsedJson
    return json.loads(path)

def constructConfig(sampleRate, languageCode, encoding):
    """
    Returns a dictionary of the configuration required for Google Cloud Speech to Text.
    """
    config = {
        "sample_rate_hertz" : sampleRate,
        "language_code" : languageCode,
        "encoding" : encoding
    }
    return config

def transcribeToText(config, cloudAudioFileUri, textOutputPath):

    client = speech_v1.SpeechClient()
    startTime = time.time()
    operation = client.long_running_recognize(config, cloudAudioFileUri)
    print(u"Transcribing .... " + cloudAudioFileUri['uri'])
    response = operation.result()

    for result in response.results:
        alternative = result.alternative[0]
        # Debug print.
        # print(u"{\n}".format(alternative.transcript))
        f = open(textOutputPath, "w+")
        f.write((u"{\n}").format(alternative.transcript))
        f.close()
        
    endTime = time.time()
    opDuration = endTime - startTime
    print("Finished " + cloudAudioFileUri['uri'] + " in " + opDuration)