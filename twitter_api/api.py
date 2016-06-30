import Insight.alchemist as alchemist
import os
import twitter as it
from twitter.api import TwitterHTTPError

class TwitterAccessMock():
    def __init__(self):
        self.api = 1

@alchemist.lead(gold=TwitterAccessMock)
class TwitterAccess(object):
    def __init__(self):
        f = open('twitter_api/simile.smile', 'r')
        self.api = TwitterHandler(f.readline()[:-1], f.readline()[:-1], f.readline()[:-1], f.readline()).twitter_access

class TwitterHandler(object):
    def __init__(self, consumerKey, consumerSecret, accessToken, accessTokenSecret):
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret
        self.accessToken = accessToken
        self.accessTokenSecret = accessTokenSecret

        print(consumerKey, consumerSecret, accessToken, accessTokenSecret)

        if not os.path.isfile('twitter_api/simile2.smile'):
            print('oauth_dance')
            token, token_key = it.oauth_dance('The Insight Project', self.consumerKey, self.consumerSecret, token_filename='twitter_api/simile2.smile')
            with open('twitter_api/simile2.smile', 'r') as f:
                token2 = f.readline()[:-1]
                token_key2 = f.readline()[:-1]
        else:
            with open('twitter_api/simile2.smile', 'r') as f:
                token = f.readline()[:-1]
                token_key = f.readline()[:-1]

        try:
            self.twitter_access = it.Twitter(auth=it.OAuth(token, token_key, self.consumerKey, self.consumerSecret))
            self.test()
        except it.TwitterHTTPError as e:
            print(e)
            raise(e)

    def test(self):
        self.twitter_access.search.tweets(q='test')
