
class OvercastFM_Failure(Exception):
    """Raised when OvercastFM returns a non acceptable Status Code"""
    def __init__(self, status_code, url):
        self.status_code = status_code
        self.url = url
        self.message = f"\nStatus Code: {status_code} \n URL: {url}\n"
        super().__init__(self.message)

class OPML_NoFeedElements(Exception):
    """Raised when XML Feed Parse returns no Elements"""
    def __init__(self):
        self.message = f"No Feed Elements."
        super().__init__(self.message)

class NoIncludedFeedsMatched(Exception):
    """Raised when no Included Feeds are Matched. Check your config.json!"""
    def __init__(self):
        self.message = f"No Matched Feeds."
        super().__init__(self.message)

class OvercastFM_TMR_FTS(Exception):    
    """Raised when OvercastFM returns a Too Many Reqests Response During First Time Setup!"""
    def __init__(self):
        self.message = f"OvercastFM returned 429: Too Many Requests during InfinitelyOvercast's First Time Setup! Try again Later."
        super().__init__(self.message)