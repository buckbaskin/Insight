'''
Created on Dec 10, 2014

@author: buck
'''

class Node(object):
    
    def __init__(self, user, dep=None):
        global connect_out
        connect_out = []
        global connect_in
        connect_in = []
        global usr
        usr = user
        global depth
        depth = dep
        global network
        network = None
    
    # connection done by reference
    def add_connect_in(self, connection):
        global connect_in
        connect_in.append(connection)
    
    def add_connect_out(self, connection):
        global connect_out
        connect_out.append(connection)
    
    def id(self):
        global usr
        return self.usr.id
    
    def set_network(self, net):
        global network
        network = net
    
class User(object):
    ''' Wrapper class for User properties
    atributes:
    unique_id: https://twitter.com/[username]
    user_name: First Last
    properties: arbitrary dict of properties that loosely follows user queries from API
    '''
    
    def __init__(self, unique_id, user_name, properties=None):
        global id
        id = unique_id
        global name
        name = user_name
        if isinstance(properties, dict):
            global props
            props = properties
