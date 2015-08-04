'''
Created on Aug 3, 2015

@author: buck

Twitter API: https://github.com/sixohsix/twitter
'''

from twitter import oauth_dance, OAuth, Twitter, TwitterStream, TwitterHTTPError
import os

'''
creates a custom Python access portal that automates a lot of the access portion
ex. streaming large datasets, maximizing data returned per API call
'''

class Twitter(object):
    def __init__(self):
        f = open('simile.smile','r')
        self.api = Twitter_Handler(f.readline()[:-1],f.readline()[:-1],f.readline()[:-1],f.readline())
        self.api.test()
        
    def get_friends_iter(self, user_id, callback):
        a = self.api
        # t.search.tweets(q=str(term), lang="en", count=100)
        followed = a.friends.list(user_id=str(user_id), count=200, skip_status='t', cursor=-1)
        callback(iter(followed['users']))
        while(followed['next_cursor']!=0):
            followed = a.friends.list(user_id=str(user_id), count=200, skip_stus='t', cursor=followed['next_cursor'])
            callback(iter(followed['users']))
        return True
    
    def get_friends_ids(self, user_id):
        a = self.api
        ids = []
        followed = a.friends.ids(user_id=str(user_id), count=5000, cursor=-1)
        ids.extend(followed)
        while(followed['next_cursor']!=0):
            followed = a.friends.list(user_id=str(user_id), count=5000, skip_stus='t', cursor=followed['next_cursor'])
            ids.extend(followed)
        return ids
    
    def get_followers_ids(self, user_id):
        a = self.api
        ids = []
        following = a.followers.ids(user_id=str(user_id), count=5000, cursor=-1)
        ids.extend(following)
        while(following['next_cursor']!=0):
            following = a.followers.list(user_id=str(user_id), count=5000, skip_stus='t', cursor=following['next_cursor'])
            ids.extend(following)
        return ids
        
class Twitter_Handler(object):
    
    def __init__(self,consumerKey,consumerSecret,accessToken,accessTokenSecret):
        self.consumer_key = consumerKey
        self.consumer_secret = consumerSecret
        self.access_token = accessToken
        self.access_token_secret = accessTokenSecret
        
        if (os.path.isfile('simile2.smile'))==False:
            print('oauth_dance')
            token,token_key = oauth_dance('The Insight Project',self.consumer_key,self.consumer_secret,token_filename='simile2.smile')
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
        global twitter_access
        try:
            twitter_access = Twitter(auth=OAuth(token, token_key, 
                                            self.consumer_key, self.consumer_secret))
            self.test()
        except TwitterHTTPError as e:
            print 'Twitter HTTP Error: '
            print e
            print 'end Twitter HTTP Error'
    
    def test(self):
        global twitter_access
        twitter_access.search.tweets(q='test')