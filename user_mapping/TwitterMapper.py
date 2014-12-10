'''
Created on Dec 10, 2014

@author: buck
'''
from user_mapping.UserNode import Node
from user_mapping.UserNode import User
from user_mapping.Network import SimpleDirectedNetwork

class BFS_Mapper(object):
    pass

class DFS_Mapper(object):
    '''Maps twitter users to a SimpleDirectedNetwork
    '''
    
    def __init__(self, net, max_depth):
        global max_depth
        max_depth = 10
        if max_depth and not max_depth < 0:
            max_depth = max_depth
        global network
        network = None
        if isinstance(net,SimpleDirectedNetwork):
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
        