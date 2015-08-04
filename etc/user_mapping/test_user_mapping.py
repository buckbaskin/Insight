from TwitterMapper import Twitter_Handler
from os import sys
from Network import SimpleDirectedNetwork
from user_mapping.TwitterMapper import BFS_Mapper

''' # Test 1: Connect to Twitter
f = open('simile.smile','r')

t = Twitter_Handler(f.readline()[:-1],f.readline()[:-1],f.readline()[:-1],f.readline())
print 'begin test1'
t.test()
print 'end test1'
'''

# Test 2: Begin mapping
print 'begin test 2'
net = SimpleDirectedNetwork()
print ('created network. isinstance(network, SimpleDirectedNetwork)? '
    +str(isinstance(net,SimpleDirectedNetwork)))
print ('network: '+str(net))
print ('network idea: '+str(net.idea()))
mapper = BFS_Mapper(net,10)
print 'created mapper'
mapper.explore('buckbaskin')

sys.exit(1)