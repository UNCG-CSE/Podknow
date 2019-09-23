import requests
from urllib.request import urlretrieve as downloadFromUrl
from pydub.utils import mediainfo


def downloadAudio(episode, path):
    """
    Given the metadata of an episode and a filepath, downloads the audio for that episode to the path.
    Returns true if the operation succeeded and false if it did not.
    """
    # TODO: Check if path ends with '\'
    fullDownloadPath = path + episode.outputFilename
    if path.exists(fullDownloadPath):
        print(episode.outputFilename + " has already been downloaded!")

    else:
        response = requests.get(episode.audioUrl)
        wasRedirect = False
        print("Attempting to download " + episode.outputFilename + " ...")
        try:
            if response.history:
                wasRedirect = True
            downloadFromUrl(response.url, fullDownloadPath)
            print("Download of " + episode.outputFilename + " was Successful!")
            episode.filePath = fullDownloadPath
            return True
        except Exception as error:
            failMsg = "Download of " + episode.outputFilename + " failed!"
            print(failMsg)
            errorStr = failMsg + "\nERROR: On attempting to download, error is as follows: " + str(error) + "\nWasRedirect: "  + wasRedirect + "\n"
            errorTxtFile = open(path+"DownloadErrorsLog.txt", "a+")
            errorTxtFile.write(errorStr)
            episode.filePath = None
            return False
    
def convertToFlac(episode):
    print("Not implemeneted")

def stereoToMono(episode):
    print("Not implemented")

def getSampleRate(audioFilePath):
    return int(mediainfo(audioFilePath)['sample_rate'])