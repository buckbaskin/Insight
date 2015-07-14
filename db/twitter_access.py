from twitter import oauth_dance, OAuth, Twitter, TwitterStream
import os
from user_model import SchemaGenerator

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
        
        self.db = 'CHANGE THIS'
        self.collection = 'CHANGE THIS TOO'
        
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
    
    def explore(self, t_user_id):
        # User to explore from (bfs)
        start = self.findOrCreateUser(t_user_id)
        # limit of number of users to explore
        limit = 1000
        # list of created users objects
        level = []
        level.append(start)
        # list of user ids to create
        plus_one = []
        while (limit > 0):
            for i in xrange(0,len(level)):
                user = level.pop()
                limit -= 1
                if not user['full_user']:
                    user = self.hydrate_user()
                if limit <= 0:
                    break
                for friend_id in self.get_friend_ids(user['t_user_id']):
                    plus_one.append(friend_id)
                    if len(plus_one) > 100: # if there are enough for one request
                        for new_user in self.bulk_init(plus_one[:100]):
                            level.append(new_user)
                        plus_one = plus_one[100:]
                    
            if len(plus_one): # clear the next level
                for new_user in self.bulk_init(plus_one):
                    level.append(new_user)
                plus_one = []
                
    def get_friend_ids(self, t_user_id):
        pass #TODO(buckbaskin)
    
    ### WRAP SCHEMA FUNCTIONS
    
    def findOrCreateUser(self, t_user_id):
        return SchemaGenerator.get_user(t_user_id, self.db, self.collection)
    
    def hydrate_user(self, t_user_id):
        pass #TODO(buckbaskin)
    
    def bulk_init(self, id_list):
        pass #TODO(buckbaskin)