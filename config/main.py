import json, os
class Config():

    __slots__ = ['json', 'includeType', 'feeds', 'bias', 'username', 'password', 'title', 'description', 'url']
    
    def __init__(self):
        self.json = json.load(open('config.json'))
        for key in self.json.keys():
            setattr(self, key, self.json[key])
