'''
Created on Dec 10, 2014

@author: buck
'''
from user_mapping.UserNode import Node
from user_mapping.UserNode import User
from user_mapping import Network
from twitter import *
import os

class BFS_Mapper(object):
    '''Maps twitter users to a SimpleDirectedNetwork via breadth first search
    
    Note: takes advantage of Twitter's API structure for batch retrieving 
		users, followers, etc.
    '''
    def __init__(self, net, max_depth_input):
        global max_depth
        if max_depth_input and not max_depth_input < 0:
            max_depth = max_depth_input
        else:
            max_depth = 10
        global network
        '''
        print ('created network. isinstance(network, SimpleDirectedNetwork)? '
                    +str(isinstance(net,Network.SimpleDirectedNetwork)))
        if not isinstance(net,Network.SimpleDirectedNetwork):
            print ('network: '+str(net))
            print ('network idea: '+str(net.idea()))
            print ('is instance now? '+str(isinstance(net,Network.SimpleDirectedNetwork)))
            print ('how about now? '+str(net.type() is Network.SimpleDirectedNetwork))
        ''' 
        if isinstance(net.idea(), int):
            network = net
        else:
            return None
        f = open('simile.smile','r')
        global twitter_object
        twitter_object = Twitter_Handler(f.readline()[:-1],f.readline()[:-1],f.readline()[:-1],f.readline())
        print 'begin access test'
        twitter_object.test()
        print 'end access test'
        

    def explore(self, source):
        node_pile = []
        if source is Node:
            self.explore_node(source,node_pile)
        elif isinstance(source,basestring):
            self.explore_string(source,node_pile, 0)
        else:
            return -1

        while(0 < len(node_pile)):
            if isinstance(node_pile[0], Node):
                self.explore_node(node_pile[0],node_pile)
                del node_pile[0]
            else:
                return -1 # only nodes should be added to the node_pile
    
    def explore_node(self, node, expansion_queue):
        global max_depth
        if node.depth is not None and node.depth < max_depth:
            # Node has connection lists
            # so get the information, make nodes for all of the connections that aren't already nodes
            # if they already have depths assigned, do nothing.
            # else assign them depth+1 and add those nodes to the node pile
            pass

    def explore_string(self, node_name, expansion_queue, depth):
        global max_depth
        # Note, should only be called for first instance
        if depth is not None and depth < max_depth:
            global twitter_access
            t = twitter_access
            friend_list = t.friends.ids()
            print 'got friends list'
            # get connections from twitter
            print 'friend ids: '+str(friend_list['ids']) +'\nlen = '+str(len(friend_list['ids']))
            print 'now to get names!'
            # make myself into a node ( assign the connections as others are built)
            
            # make connections into nodes (this will only be called first)           
            # Node has connection lists
            # assign them depth = 1 and add those nodes to the node pile
            pass

class DFS_Mapper(object):
    '''Maps twitter users to a SimpleDirectedNetwork via depth first search
    '''
    
    def __init__(self, net, max_depth_input):
        global max_depth
        if max_depth_input and not max_depth_input < 0:
            max_depth = max_depth_input
        else:
            max_depth = 10
        global network
        network = None
        if isinstance(net,Network.SimpleDirectedNetwork):
            network = net
        
    def explore(self, source):
        depth = 0
        if source is Node:
            # explores node
            self.explore_node(source,0)
                
            
    def explore_node(self, node, depth):
        # User and properties present (enough) in node form
        global max_depth
        if depth < max_depth:
            connections = node.connect_out+node.connect_in
            for neighbor in connections:
                if neighbor.network is None: #unexplored
                    if isinstance(neighbor, Node):
                        self.explore_node(neighbor, depth+1)
                    if isinstance(neighbor, str):
                        self.explore_twitter(neighbor, depth+1)
        network.add_node(node)
                    
                
    
    def explore_twitter(self, screen_name, depth):
        u = User()
        node = Node(u)
        # TODO (buck) get Twitter Interface from Data collection hooked up
        # get users/show <- screen_name
        # get unique id (https://twitter.com/[screen_name])
        # get name
        # get friends/followers, add to connection lists as strings (first convert ids to screennames)
        '''Food for thought:
        if I'm already getting everyone's user profile to get their screennames, maybe bfs makes more sense
        '''
        # create dict of other properties
        
        #then call the explore node on the created version
        self.explore_node(node,depth)
        
class Twitter_Handler(object):
    
    def __init__(self,consumerKey,consumerSecret,accessToken,accessTokenSecret):
        print 'created handler object'
        global consumer_key
        consumer_key = consumerKey
        #print consumer_key
        global consumer_secret
        consumer_secret = consumerSecret
        #print consumer_secret
        global access_token
        access_token = accessToken
        #print access_token
        global access_token_secret
        access_token_secret = accessTokenSecret
        #print access_token_secret
        
        if (os.path.isfile('simile2.smile'))==False:
            print('oauth_dance')
            token,token_key = oauth_dance('The Insight Project',consumer_key,consumer_secret,token_filename='simile2.smile')
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
                                            consumer_key, consumer_secret))
            twitter_access.search.tweets(q='test')
        except TwitterHTTPError as e:
            print 'Twitter HTTP Error: '
            print e
            print 'end Twitter HTTP Error'
        print 'end create twitter object'
    
    def test(self):
        global twitter_access
        twitter_access.search.tweets(q='test')