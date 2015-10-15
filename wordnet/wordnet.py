'''
Created on Oct 15, 2015

@author: buck
'''

import math

class WordNetwork(object):
    def __init__(self):
        self.vertices = {}
        
    def add_vertex(self, word):
        if word not in self.vertices:
            self.vertices[word] = Wordlet(word)
            
    def add_edge(self, first, second):
        if first not in self.vertices:
            self.add_vertex(first)
        if second not in self.vertices:
            self.add_vertex(second)
        # print 'adding edge: '+str(first)+' -> '+str(second)
        self.vertices[first].add_trailer(second)    
        self.vertices[second].add_leader(first)
        
    def reduce_network(self, similarity, iterations):
        # similarity indicates tolerance for isomorphic like relations
        # 1>=: only take words that are connected with the exact same words
        # 0: take words that are connected to at least one of the same word or synonyms (previously identified reductions)
        
        # similarity not yet implemented
        count = 0
        l = len(self.vertices)
        for word, _ in self.vertices.iteritems():
            count += 1
            if count % int(math.floor(l/100)) == 0:
                print str(int(math.ceil((count*100.0)/l)))+' %'
            self.find_similar_words(word)
    
    def print_network(self):
        for key, value in self.vertices.iteritems():
            print (str(key)+' '*20)[:20]+ ' -> ..'+str(len(value.next))
            for k, v in value.next.iteritems():
                print (str(v)+'     ')[:5]+' -> '+str(k)
                
    def print_similarity(self):
        avg = 0
        count = 0
        maximum = 0
        maxstring = ''
        for word, wordlet in self.vertices.iteritems():
            if len(wordlet.similar_words):
                for word_, strength in wordlet.similar_words.iteritems():
                    count += 1
                    avg += strength
                    if strength > maximum:
                        maximum = strength
                        maxstring = str(word)+' -> '+str(word_)+' ... '+str(strength)
                    if strength > 5:
                        print str(word)+' -> '+str(word_)+' ... '+str(strength) 
        print 'avg = '+str(avg*1.0/count)
        print 'max = '+str(maximum)+' '+str(maxstring)
    
    def find_similar_words(self, word): # first iteration
        preCandidates = {}
        postCandidates = {}
        wordlet = self.vertices[word]
        
        for word_, count in wordlet.prev.iteritems(): # backward references
            for word_option, count_ in self.vertices[word_].next.iteritems(): # forward references back to the same point
                similarity = min(count, count_) # overlap between forward, backward references
                if word_option in preCandidates:
                    preCandidates[word_option] = max(preCandidates[word_option], similarity)
                else:
                    preCandidates[word_option] = max(0, similarity)
        
        for word_, count in wordlet.next.iteritems(): # backward references
            for word_option, count_ in self.vertices[word_].prev.iteritems(): # forward references back to the same point
                similarity = min(count, count_) # overlap between forward, backward references
                if word_option in postCandidates:
                    postCandidates[word_option] = max(postCandidates[word_option], similarity)
                else:  
                    postCandidates[word_option] = max(0, similarity)
                
        for word_, count in preCandidates.iteritems():
            if word_ in postCandidates:
                
                if not (word_ == word):
                    wordlet.similar_words[word_] = max(count, postCandidates[word_])
        
    
class Wordlet(object):
    def __init__(self, word):
        self.word = word
        self.prev = {}
        self.next = {}
        
        self.similar_words = {}
        
    def add_trailer(self, word):
        if word in self.next:
            self.next[word] += 1
        else:
            self.next[word] = 1
            
    def add_leader(self, word):
        if word in self.prev:
            self.prev[word] += 1
        else:
            self.prev[word] = 1