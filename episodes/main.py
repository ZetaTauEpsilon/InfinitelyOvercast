class ListenedEpisode():
    def __init__(self, timestamp, pubdate, title, url):
        self.timestamp = timestamp
        self.pubdate =  pubdate
        self.title = title
        self.url = url

class FeedEpisode():

    def __init__(self, title, url, pubdate, raw):
        self.title = title
        self.url = url
        self.pubdate = pubdate
        self.raw = raw
    
    def __repr__(self):
        return f"""
        title: {repr(self.title)}
        url: {repr(self.url)}
        """