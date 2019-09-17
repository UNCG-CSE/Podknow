from abc import ABC, abstractmethod

class WebscraperPage(ABC):

    def __init__(self, podcastId):
        self.podcastId = podcastId

    @abstractmethod
    def scrapeEpisodeList(self):
        return None
        
    @abstractmethod
    def scrapeLatestEpisode(self):
        return None

    @abstractmethod
    def scrapeTrendingEpsiode(self):
        return None
