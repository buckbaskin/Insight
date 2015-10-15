'''
Created on Oct 15, 2015

@author: buck
'''

from wordnet import Wordlet, WordNetwork
import re

def intake_local_text(f, network=WordNetwork()):
    first = ''
    second = '<start>'
    iterator = iter(text_divide(f))
    while second is not None:
        first = second
        second = iterator.next()
        if second is None:
            break
        if second == '<full_stop>' and first == '<full_stop>':
            pass
        elif second == '<full_stop>':
            network.add_edge(first, '<end>')
        elif first == '<full_stop>':
            network.add_edge('<start>', second)
        else:
            network.add_edge(first, second)
    return network

def text_divide(f):
    # a generator that yields items instead of returning a list
    pattern = re.compile('[\W_]+')
    text = open(f, 'r')
    for line in text:
        s = line.split()
        for token in s:
            token = token.lower()
            # print 'token: '+str(token)+' [-1]: '+str(token[-1])
            if len(token) > 2 and token[-1] == '.':
                token = re.sub(r'\W+', '', token)
                yield token
                yield '<full_stop>'
            else:
                token = re.sub(r'\W+', '', token)
                yield token
    yield '<end>'
    yield None