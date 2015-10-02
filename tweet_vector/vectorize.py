'''
Created on Oct 1, 2015

@author: buckbaskin
'''

class TweetVector(object):
    def __init__(self, tweet):
        # tweet is the string of 140ish characters
        self.tkns = self.tokenize(tweet)
        
    def tokenize(self, tweet):
        items = tweet.split()
        for i in range(len(items)):
            if items[i] == '<start>':
                items[i] = 'start'
        return items
    
    def vectorize(self, tkns):
        index = 0
        sparse_vec = {'<start>':0}
        for t in tkns:
            index += 1
            sparse_vec[t] = index
            
    def distance(self, other_vec):
        # determine the distance in word+word dimensional space
        # if a word is in both tweets:
        #    the distance for that word is the delta between locations squared
        # else:
        #    the distance for that word is the length of the longer tweet squared
        # normalize over the maximum possible distance (length of longer tweet squared * (sum of length of tweets))
        return 0
        
    def min_modulo_distance(self):
        # test every possible rotational permutation of the ordering against this tweet
        # return the minimum distance
        return 0
    
    def min_reorder_distance(self):
        # reorder both tweets based on probability model of tweet construction
        # return the distance between reordered tweets
        return 1
    
def test():
    t = TweetVector('a b <start>')
    return t.tkns[2] == 'start'

if __name__ == '__main__':
    print 'was the test succesful? ' + str(test())