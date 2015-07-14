from twitter import *
import os
import collections

class access(object):
    def __init__(self,consumerKey,consumerSecret,accessToken,accessTokenSecret):
        self.consumer_key = consumerKey
        self.consumer_secret = consumerSecret
        self.access_token = accessToken
        self.access_token_secret = accessTokenSecret
        
        if (os.path.isfile('simile2.smile'))==False:
            print('oauth_dance')
            token,token_key = oauth_dance('The Insight Project',self.consumer_key,self.consumer_secret,token_filename='simile2.smile')
        else:
            with open('simile2.smile','r') as f:
                token = f.readline()[:-1]
                token_key = f.readline()
        self.twitter_object = Twitter(auth=OAuth(token, token_key, self.consumer_key, self.consumer_secret))
        self.twitter_object.search.tweets(q='test')
        self.twitter_stream = TwitterStream(auth=OAuth(token, token_key, self.consumer_secret, self.consumer_key))
        
    def search(self,query,                              #query
               language='en',result_type='recent',      #tweet modifiers
               extra_info=False):
        t = self.twitter_object
        try:
            return t.search.tweets(q=query,
                                            lang='en',
                                            count=100,
                                            include_entities=False,
                                            result_type = 'recent')
        except Exception as e:
            print(str(e))
            
    def stream(self, keywords,tags=list(),users=list()):
        pass