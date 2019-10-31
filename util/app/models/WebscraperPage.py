from urllib.request import urlopen as uRequest
from urllib.request import urlretrieve as downloadFromUrl
from abc import ABC, abstractmethod

class WebscraperPage(ABC):

    def __init__(self, podcastId, rootUrl):
        self.podcastId = podcastId
        self.rootUrl = rootUrl
        self.downloadRawHtml()
        self.scrapeEpisodeList()
        self.scrapeLatestEpisode()
        self.scrapeTrendingEpsiode()

    @abstractmethod
    def downloadRawHtml(self):
        webClient = uRequest(self.rootUrl+self.podcastId)
        page_rawhtml = webClient.read()
        webClient.close()
        self.page = page_rawhtml

    @abstractmethod
    def scrapeEpisodeList(self):
        self.episodeList = None
        
    @abstractmethod
    def scrapeLatestEpisode(self):
        self.latestEpisode = None

    @abstractmethod
    def scrapeTrendingEpsiode(self):
        self.trendingEpisode = None


