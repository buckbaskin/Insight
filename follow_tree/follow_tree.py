'''
Created on Aug 3, 2015

@author: buck

Twitter API: https://github.com/sixohsix/twitter
'''

from insight_apis.twitter_access import TwitterAccess
import threading
import time
import sys

'''
creates a data structure for analyzing the time based expansion of interests on Twitter
'''

def list_to_dict(l):
    d = dict()
    for element in l:
        d[int(element)] = 'exists'
    return d

class FollowTree(object):
    def __init__(self, root_id):
        self.access = TwitterAccess()
        print 'followTree: twitter access equipped'
        self.root = FollowNode(root_id, self.access)
        print 'followTree: root created'
    
    def build(self):
        def _build(root):
            counter = 0
            interests = root.follows()
            sys.stdout.write('got interests:')
            for user_id in interests:
                counter += 1
                sys.stdout.write('adding node '+str(counter)+' to root')
                self._add(FollowNode(user_id, self.access))
                self.traverse(self.root, 'interest path after build: ')
                time.sleep(60)
        
#         thread = FollowThread(_build, (self.root,))
#         print 'build thread.start_new_thread'
#         thread.start()
#         print 'build thread.end'
        print 'blocking build:'
        _build(self.root)
        
    def _add(self, element):
        if(len(self.root.tree_followers)):
            for node_id in self.root.tree_followers:
                # if a given node follows the element to be inserted, make it follow element, rm from following root
                if element.followed_by(node_id):
                    element.add_follower(self.root.tree_followers[node_id])
                    del self.root.tree_followers[node_id]
        print 'adding element '+element.user+' to '+self.root.user
        self.root.tree_followers[element.user] = element
        
    def traverse(self, root, string, new_print):
        if(len(root.tree_followers)):
            for child_id in root.tree_followers:
                child = root.tree_followers[child_id]
                self.traverse(child, string+' '+root.user)
        else:
            new_print(string+' end '+root.user)

class FollowNode(object):
    def __init__(self, user_id, access):
        self.user = str(user_id)
        self.followers = list_to_dict(access.get_followers_ids(self.user))
        self.friends = list_to_dict(access.get_friends_ids(self.user))
        print 'user '+str(user_id)+' has '+str(len(self.followers))+' follwers and '+str(len(self.friends))+' friends'
        self.tree_followers = dict()
        
    def follows(self, user_id=False):
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

class FollowThread(threading.Thread):
    def __init__ (self, function, arg):
        threading.Thread.__init__(self)
        self.f = function
        self.a = arg

    def run(self):
        self.f(self.a)
    