'''
Created on Dec 10, 2014

@author: buck
'''
from user_mapping.UserNode import Node
from user_mapping.UserNode import User
from user_mapping.Network import SimpleDirectedNetwork

class BFS_Mapper(object):
    '''Maps twitter users to a SimpleDirectedNetwork via breadth first search
    
    Note: takes advantage of Twitter's API structure for batch retrieving 
		users, followers, etc.
    '''
    def __init__(self, net, max_depth):
        global max_depth
        max_depth = 10
        if max_depth and not max_depth < 0:
            max_depth = max_depth
        global network
        if isinstance(net, SimpleDirecterNetwork):
            network = net

    def explore(self, source):
        depth = 0
        node_pile = []
        if source is Node:
            self.explore_node(source,node_pile)
		elif isinstance(source,basestring):
            self.explore_twitter(source,node_pile)
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

    def explore_twitter(self, node, expansion_queue, depth):
		global max_depth
        if node.depth is not None and node.depth < max_depth:
            # get connections from twitter
            # make myself into a node ( assign the connections as others are built)
            # make connections into nodes (this will only be called first)           
			# Node has connection lists
            # assign them depth = 1 and add those nodes to the node pile
            pass

class DFS_Mapper(object):
    '''Maps twitter users to a SimpleDirectedNetwork via depth first search
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
        
