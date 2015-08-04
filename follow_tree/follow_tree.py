'''
Created on Aug 3, 2015

@author: buck

Twitter API: https://github.com/sixohsix/twitter
'''

from api.twitter import Twitter

'''
creates a data structure for analyzing the time based expansion of interests on Twitter
'''

def list_to_dict(list):
    pass
    

class FollowTree(object):
    def __init__(self, root_node):
        self.explored = dict()
        self.tree = dict()
        self.root = root_node
        self.access = Twitter()
    
    def build(self):
        interests = self.root_node.follows()
        for user_id in interests:
            self._add(FollowNode(user_id, self.access))
        
    def _add(self, element):
        pass # TODO(buckbaskin): add element to the correct branch

class FollowNode(object):
    def __init__(self, user_id, access):
        self.user = str(user_id)
        self.followers = list_to_dict(access.get_followers_ids(self.user))
        self.friends = list_to_dict(access.get_friends_ids(self.user))
        
    def follows(self, user_id):
        if(user_id):
            return user_id in self.friends
        else:
            return self.friends
        
    def followed_by(self, user_id):
        if(user_id):
            return user_id in self.followers
        else:
            return self.followers
        