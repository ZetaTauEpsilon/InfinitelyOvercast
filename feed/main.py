import podcastparser, urllib
from lxml import etree
from episodes.main import FeedEpisode

class Feed():

    def __init__(self, url, title):
        self.title = title
        self.parsed = podcastparser.parse(url, urllib.request.urlopen(url))
        self.raw = etree.parse(urllib.request.urlopen(url))
        self.parseFeed()

    def parseFeed(self):
        self.episodes = list(map(self.pullEpisode, self.parsed['episodes']))
    
    def pullEpisode(self, episode):
        return FeedEpisode(episode['title'], episode['link'], episode['published'], episode)