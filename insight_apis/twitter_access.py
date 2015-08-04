'''
Created on Aug 3, 2015

@author: buck

Twitter API: https://github.com/sixohsix/twitter
'''

import twitter as it
# import twitter.Twitter as Twitter
# import twitter.OAuth as OAuth
# import twitter.TwitterHTTPError as TwitterHTTPError
# import twitter.oauth_dance as oauth_dance
import os
from twitter.api import TwitterHTTPError

'''
creates a custom Python access portal that automates a lot of the access portion
ex. streaming large datasets, maximizing data returned per API call
'''

class TwitterAccess(object):
    def __init__(self):
        f = open('../insight_apis/simile.smile','r')
        self.api = Twitter_Handler(f.readline()[:-1],f.readline()[:-1],f.readline()[:-1],f.readline()).twitter_access
        
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
        try:
            followed = a.friends.ids(user_id=str(user_id), count=5000, cursor=-1)
        except TwitterHTTPError as the:
                print the
                print 'probably terminated because of rate limit'
                exit()
        ids.extend(followed['ids'])
        while(followed['next_cursor']!=0):
            try:
                followed = a.friends.ids(user_id=str(user_id), count=5000, cursor=followed['next_cursor'])
            except TwitterHTTPError as the:
                print the
                print 'probably terminated because of rate limit'
                exit()
            ids.extend(followed['ids'])
        return ids
    
    def get_followers_ids(self, user_id):
        a = self.api
        ids = []
        try:
            follows = a.followers.ids(user_id=str(user_id), count=5000, cursor=-1)
        except TwitterHTTPError as the:
            print the
            print 'probably terminated because of rate limit'
            exit()
        ids.extend(follows['ids'])
        while(follows['next_cursor']!=0):
            try:
                follows = a.followers.ids(user_id=str(user_id), count=5000, cursor=follows['next_cursor'])
            except TwitterHTTPError as the:
                print the
                print 'probably terminated because of rate limit'
                exit()
            ids.extend(follows['ids'])
        return ids
        
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
        
def main():
    ta = TwitterAccess()
    
if __name__ == '__main__':
    main()