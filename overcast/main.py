import requests, os, exceptions
from datetime import datetime
from lxml import etree
from episodes.main import ListenedEpisode

OVERCAST_LOGIN_URL = 'https://overcast.fm/login'
OVERCAST_OPML_EXTENDED_URL = 'https://overcast.fm/account/export_opml/extended'

class OvercastAccount():

    __slots__ = ['session', 'opml_file', 'last_pull']

    def __init__(self, username, password):
        self.last_pull = 0
        self.session = requests.Session()
        self.login(username, password)
        self.opml_file = self.getOPML()
    
    def login(self, username, password):
        s = self.session.post(OVERCAST_LOGIN_URL, data={'then':'account', 'email':username, 'password':password})
        if s.status_code != 200:
            raise exceptions.OvercastFM_Failure(s.status_code, s.url)
    
    def getOPML(self):
        if (datetime.now().timestamp()-self.last_pull) <= 60*15:
            return 'overcast.opml'
        else:
            try:
                opmlData = self.session.get(OVERCAST_OPML_EXTENDED_URL, allow_redirects=True)
                if opmlData.status_code == 200:
                    self.last_pull = datetime.now().timestamp()
                    open('overcast.opml', 'wb').write(opmlData.content)
                    return 'overcast.opml'
                else:
                    raise exceptions.OvercastFM_Failure(opmlData.status_code, opmlData.url)
            except exceptions.OvercastFM_Failure:
                if os.path.exists('overcast.opml'):
                    return 'overcast.opml'
                else:
                    raise exceptions.OvercastFM_TMR_FTS()

class OvercastParsing():

    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.parsed = etree.parse(self.file)
    
    def getSubscribedFeedNodes(self):
        output = self.parsed.xpath("./body/outline[@text='feeds']/*")
        if len(output) > 0:
            return output
        else:
            raise exceptions.OPML_NoFeedElements()
    
    def convertOvercastItem(self, outline):
        return ListenedEpisode(
            self.overcastTimeToEpoch(outline.get('userUpdatedDate')),
            self.overcastTimeToEpoch(outline.get('pubDate')),
            outline.get('title'), 
            outline.get('enclosureUrl')
            )
    
    def overcastTimeToEpoch(self, timestring):
        return datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%S%z")
    
    def matchIncludedFeed(self, config, node):
        if config.includeType == 'overcastID':
            return (False, True)[bool(node.get('overcastId') in config.feeds)]
        if config.includeType == 'title':
            return (False, True)[bool(node.get('title') in config.feeds)]
        else:
            raise exceptions.NoIncludedFeedsMatched
    
    def buildRecentlyListened(self, config, feedNodes): # ! GENERATOR FUNCTION, list of maps
        for node in feedNodes:
            if self.matchIncludedFeed(config, node):
                yield map(self.convertOvercastItem, node)
