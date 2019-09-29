import requests
from urllib.request import urlretrieve as downloadFromUrl

class PodcastEpisode:
    """
    PodcastEpisode is a class that holds all relevant metadata for a podcast episode.
    A webscraper or an API call will return this object.
    """

    def __init__(self, id, podcastName, date, episodeTitle, audioUrl):
        self.id = id
        self.podcastName = podcastName
        self.episodeDate = date
        self.episodeTitle = episodeTitle
        self.audioUrl = audioUrl
        self.initExt()
        self.initFileName()

    def initExt(self):
        self.audioExt = ""
        if ".mp3" in self.audioUrl:
            self.audioExt = ".mp3"
        elif ".wav" in self.audioUrl:
            self.audioExt = ".wav"
        elif ".ogg" in self.audioUrl:
            self.audioExt = ".ogg"
        elif ".m4a" in self.audioUrl:
            self.audioExt = ".m4a"
    
    def initFileName(self):
        self.outputFilename = str(self.id)+"_"+self.podcastName+"_"+self.episodeDate+"_"+self.episodeTitle+self.audioExt

    def __repr__(self):
        return self.outputFilename

        
        
