'''
Created on Dec 10, 2014

@author: buck

Twitter API: https://github.com/sixohsix/twitter
'''

from twitter import *
import os

'''
Currently generates a list of associated words (some are relevant)

Todo: increase relevant word count
 - remove words that are common across all datasets
 - combine words that are the same? ex. robot/robots
 - score words based on distance from the search word in the tweet
'''

class AssociationLookup(object):
    def __init__(self, debug=False):
        f = open('simile.smile','r')
        self.twitter_object = Twitter_Handler(f.readline()[:-1],f.readline()[:-1],f.readline()[:-1],f.readline())
        if debug:
            print 'begin access test'
        self.twitter_object.test()
        if debug:
            print 'end access test'
    
    def collect_one(self, term): # process one term
        # process in previous data for that term
        try:
            f = open(self.full_file_path(term),'r')
        except IOError:
            f = open(self.full_file_path(term),'w')
            f.close()
            f = open(self.full_file_path(term),'r')
        content_file = f
        content_dict = self.read_in(content_file)
        # collect tweets with that term
        global twitter_access
        t= twitter_access
        tweets = t.search.tweets(q=str(term), lang="en", count=100)['statuses']
        # iterate through data, merging with existing data
        for tweet in tweets:
            for item in tweet['text'].split():
                self.add_content(item, 1, content_dict)
        # write the data out to the file
        content_file = open(self.full_file_path(term),'w')
        self.write_out(content_dict, content_file)
        content_file.close()
        
        # print "Done with search for "+term
        
    def read_in(self, open_file):
        data = dict()
        # print "read in started"
        for line in open_file.readlines():
            # print line
            try:
                word, count = line.split('|')
            except ValueError:
                print "failed to include line: "+str(line).rstrip("\n")+" split: "+str(line.split('|'))
            data[word] = int(count.rstrip('\n'))
        # print "read in ended"
        return data
    
    def add_content(self, content, weight, content_dict):
        try:
            key = self.key_clean(str(content))
            if(self.invalid_key(key)):
                return
        except:
            return
        try:
            data = int(content_dict[key])
        except KeyError:
            content_dict[key] = 0
            data = int(content_dict[key])
        try:
            content_dict[key] = int(data) + int(weight)
        except Exception as e:
            print e
            print "key: "+str(key)+" data: "+str(data)+" weight: "+str(weight)
            raise(e)
    
    def write_out(self, data, open_file):
        for key in iter(data):
            open_file.write(str(key)+'|'+str(data[key])+'\n')
            
    def dict_by_value(self, dictionary):
        sorted_dict = sorted(dictionary.items(), key=lambda x: x[1], reverse=True) # sorts on the second item (value)
        # print "sorted_dict:"+str(sorted_dict)
        return sorted_dict
    
    def full_file_path(self, term):
        return ("data/"+term.replace(" ","_")+"_association.txt").lower()
    
    def invalid_key(self, key):
        if(len(key)<=2):
            return True
        baddies = ['the', 'camp']
        for check in baddies:
            if(check == key):
                return True
        bad_parts = ['1','2','3','4','5','6','7','8','9','0','"',"'","[","@","#","&amp;"]
        for check in bad_parts:
            if check in key:
                return True
        return False
    
    def key_clean(self, key):
        mod_key = key.replace("@","").replace("#","").replace("[","").replace("]","").replace("'","").replace("\"","").lower()
        mod_key = mod_key.replace(",","").replace("?","").replace(":","").replace("http://","").replace("https://","")
        return mod_key
        
        
        
class Twitter_Handler(object):
    
    def __init__(self,consumerKey,consumerSecret,accessToken,accessTokenSecret, debug=False):
        if(debug):
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
        if(debug):
            print 'end create twitter object'
    
    def test(self):
        global twitter_access
        twitter_access.search.tweets(q='test')