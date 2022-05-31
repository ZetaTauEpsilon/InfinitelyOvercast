from overcast.main import OvercastAccount, OvercastParsing
from feed.main import Feed
import random, itertools

class Queue():

    def __init__(self, config):
        self.config = config
        self.main()
    
    def main(self):
        self.account = OvercastAccount('zedicola@comcast.net','1201Zack10319') # TODO: move to config
        self.parser = OvercastParsing(self.account.opml_file)
        self.importedFeedNodes = self.parser.getSubscribedFeedNodes()
        self.recentlyListened = self.parser.buildRecentlyListened(self.config, self.importedFeedNodes) 
        self.queue = self.buildEligibilityLists()

    def buildEligibilityLists(self):
        self.allIncludedEpisodes = list(self.pullAllIncludedFeeds())
        self.unlistened = self.allIncludedEpisodes.copy()
        self.popRecentlyListened()
        if self.config.bias == "random":
            return random.shuffle(self.unlisted)
        if self.config.bias == "newest":
            return self.unlisted.sort(key=lambda e: e.pubdate, reverse=True)
        if self.config.bias == "oldest":
            return self.unlisted.sort(key=lambda e: e.pubdate)
        if self.config.bias == "default":
            return self.defaultSort()
    
    def popRecentlyListened(self):
        for episode in self.allIncludedEpisodes:
            self.unlistened = [i for i in self.unlistened if i.title == episode.title]
    
    def popFreshEpisodes(self):
        self.rottenEpisodes = self.allIncludedEpisodes_ByPubdateNewest.copy()
        for episode in self.freshEpisodes:
            for e in self.rottenEpisodes:
                if episode.title == e.title:
                    self.rottenEpisodes.pop(self.rottenEpisodes.index(e))

    def pullAllIncludedFeeds(self):
        for node in self.importedFeedNodes:
            if self.parser.matchIncludedFeed(self.config, node):
                for e in Feed(node.get('xmlUrl'), node.get('title')).episodes:
                    yield e
    
    def defaultSort(self):

        self.allIncludedEpisodes_ByPubdateNewest = sorted(
                self.allIncludedEpisodes,
                key=lambda e: e.pubdate, 
                reverse=True
            )
        
        self.allRecentlyListened_ByPubdateNewest = sorted(
                list(
                    itertools.chain.from_iterable(
                            self.recentlyListened
                        )
                    ),
                key=lambda e: e.pubdate, 
                reverse=True
            )

        self.freshEpisodes = list(
                self.yieldFresh()
            )
        self.popFreshEpisodes()
        random.shuffle(self.rottenEpisodes)
        for episode in self.rottenEpisodes:
            self.freshEpisodes.append(episode)
        return self.freshEpisodes

    def yieldFresh(self): # ! GENERATOR
        for ep in self.allIncludedEpisodes_ByPubdateNewest:
            if ep.pubdate > self.allRecentlyListened_ByPubdateNewest[0].pubdate.timestamp():
                yield ep

class OutputGenerator():
    def __init__(self, queue, config):
        self.queue = queue
        self.config = config
    
    def buildXMLEntries(self, feed):
        for item in self.queue.queue:
            entry = feed.add_entry()
            entry.title(item.title)
            entry.description(item.raw['description'])
            entry.link(href=item.url)
            entry.guid(item.url, permalink=True)
            try:
                entry.podcast.itunes_image(item.raw['episode_art_url'])
            except:
                continue
            for e in item.raw['enclosures']:
                entry.enclosure(e['url'], str(e['file_size']), e['mime_type'])