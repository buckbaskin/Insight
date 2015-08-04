'''
Created on Aug 3, 2015

@author: buck

Twitter API: https://github.com/sixohsix/twitter
'''

from insight_apis.twitter_access import TwitterAccess

'''
creates a data structure for analyzing the time based expansion of interests on Twitter
'''

def list_to_dict(l):
    d = dict()
    for element in l:
        d[element.user] = element
    return d

class FollowTree(object):
    def __init__(self, root_id):
        self.access = TwitterAccess()
        self.root = FollowNode(root_id, self.access)
    
    def build(self):
        interests = self.root_node.follows()
        for user_id in interests:
            self._add(FollowNode(user_id, self.access))
        
    def _add(self, element):
        if(len(self.root.tree_followers)):
            for node_id in self.root.tree_followers:
                # if a given node follows the element to be inserted, make it follow element, rm from following root
                if element.followed_by(node_id):
                    element.add_follower(self.root.tree_followers[node_id])
                    del self.root.tree_followers[node_id]
        self.root.tree_followers[element.user] = element

class FollowNode(object):
    def __init__(self, user_id, access):
        self.user = str(user_id)
        self.followers = list_to_dict(access.get_followers_ids(self.user))
        self.friends = list_to_dict(access.get_friends_ids(self.user))
        self.tree_followers = dict()
        
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
    
    def add_follower(self, user_node):
        self.tree_followers[user_node.user] = user_node
        
    def height(self):
        max_height = 0
        for node in self.tree_followers:
            if(node.height()>max_height):
                max_height = node.height  
        return max_height