import requests
from urllib.request import urlretrieve as downloadFromUrl

class PodcastEpisode:

    def __init__(self, id, podcastName, date, episodeTitle, audioUrl):
        self.id = id
        self.podcastName = podcastName
        self.episodeDate = date
        self.episodeTitle = episodeTitle
        self.audioUrl = audioUrl
        self.initScrubMeta()
        self.initExt()
        self.initFileName()
    
    def downloadAudio(self, path):
        # TODO: Check if path ends with '\'
        fullDownloadPath = path+self.OutputFilename

        if path.exists(fullDownloadPath):
            print(self.OutputFilename + " has already been downloaded!")

        else:
            response = requests.get(self.audioUrl)
            wasRedirect = False
            print("Attempting to download " + self.OutputFilename + " ...")
            try:
                if response.history:
                    wasRedirect = True
                downloadFromUrl(response.url, fullDownloadPath)
                print("Download of " + self.OutputFilename + " was Successful!")
                self.filePath = fullDownloadPath
                return True
            except Exception as error:
                failMsg = "Download of " + self.OutputFilename + " failed!"
                print(failMsg)
                errorStr = failMsg + "\nERROR: On attempting to download, error is as follows: " + str(error) + "\nWasRedirect: "  + wasRedirect + "\n"
                errorTxtFile = open(path+"DownloadErrorsLog.txt", "a+")
                errorTxtFile.write(errorStr)
                self.filePath = None
                return False

    def initExt(self):
        self.audioExt = ""
        if ".mp3" in self.audioUrl:
            self.audioExt = ".mp3"
        elif ".wav" in self.audioUrl:
            self.audioExt = ".wav"
        elif ".ogg" in self.audioUrl:
            self.audioExt = ".ogg"
    
    def initScrubMeta(self):
        # TODO: Scrub meta of all illegal filename characters.
        return None
    
    def initFileName(self):
        self.OutputFilename = str(self.id)+"_"+self.podcastName+"_"+self.episodeDate+"_"+self.episodeTitle+self.audioExt

        
        
