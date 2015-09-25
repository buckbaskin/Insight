'''
Twitter Manager handles all requests for data from twitter
Analysis is run separately, and is run over all data collected/in db up to that point.
The two functions run asynchronously, but Analysis may request data (run task that puts a task into data Queue)

Twitter Manager makes requests on list
Twitter API: https://github.com/sixohsix/twitter

This is properly used by creating a TwitterManager and passing it as an arg to tasks that need it
'''
import time
import os
import twitter as it
from twitter.api import TwitterHTTPError

class TwitterManager(object):
    
    # TODO define error classes in this class that help other classes define rate limits, etc.
    
    def __init__(self):
        self.new_requests = []
        self.full_requests = []
        self.partial_requests = {}
        
        f = open('../insight_apis/simile.smile','r')
        self.api = Twitter_Handler(f.readline()[:-1],f.readline()[:-1],f.readline()[:-1],f.readline()).twitter_access
        
    def get_api(self):
        return self.api.twitter_access
        
class Twitter_Handler(object):
    
    def __init__(self,consumerKey,consumerSecret,accessToken,accessTokenSecret):
        self.consumer_key = consumerKey
        self.consumer_secret = consumerSecret
        self.access_token = accessToken
        self.access_token_secret = accessTokenSecret
        
        if (os.path.isfile('simile2.smile'))==False:
            print('oauth_dance')
            token,token_key = it.oauth_dance('The Insight Project',self.consumer_key,self.consumer_secret,token_filename='simile2.smile')
            '''testing'''
            with open('simile2.smile','r') as f:
                token2 = f.readline()[:-1]
                token_key2 = f.readline()[:-1]
            print '|'+token+'|'
            print '|'+token2+'|'
            print '|'+token_key+'|'
            print '|'+token_key2+'|'
            '''end testing code'''
        else:
            with open('simile2.smile','r') as f:
                token = f.readline()[:-1]
                token_key = f.readline()[:-1]
        try:
            self.twitter_access = it.Twitter(auth=it.OAuth(token, token_key, 
                                            self.consumer_key, self.consumer_secret))
            self.test()
        except it.TwitterHTTPError as e:
            print 'Twitter HTTP Error: '
            print e
            print 'end Twitter HTTP Error'
    
    def test(self):
        self.twitter_access.search.tweets(q='test')
        
        
def initialize():
    return TwitterManager()