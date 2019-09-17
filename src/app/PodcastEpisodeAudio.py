import PodcastEpisode
import requests
from urllib.request import urlretrieve as downloadFromUrl

class PodcastAudio:
    """
    PodcastAudio is a class of static methods that deal with podcast audio files.
    """

    @staticmethod
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
    
    @staticmethod
    def convertToFlac(episode):
        print("Not implemeneted")

    @staticmethod
    def stereoToMono(episode):
        print("Not implemented")