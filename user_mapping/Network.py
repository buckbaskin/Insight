'''
Created on Dec 10, 2014

@author: buck
'''
from user_mapping.UserNode import Node



class SimpleDirectedNetwork(object):
    
    def __init__(self):
        global nodes
        nodes = []
    
    def add_node(self, new_node):
        ''' Adds in a new node and updates references/connections
        '''
        nodes.append(new_node)
        new_node.set_network(self)
        for existing_node in nodes:
            for out_connections in existing_node.connect_out:
                if out_connections is str:
                    if out_connections == new_node.id():
                        new_node.add_connect_in(existing_node)
                        out_connections = new_node
                        break
                elif out_connections is Node:
                    if out_connections == new_node:
                        new_node.add_connect_in(existing_node)
                        break
            for out_connections in new_node.connect_out:
                if out_connections is str:
                    if out_connections == existing_node.id():
                        existing_node.add_connect_in(new_node)
                        out_connections = existing_node
                        break
                elif out_connections is Node:
                    if out_connections == existing_node:
                        existing_node.add_connect_in(new_node)
                        break
                    