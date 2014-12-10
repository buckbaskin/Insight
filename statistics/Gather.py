from twitter import *
from twitter.api import TwitterHTTPError
import os
import collections
from math import ceil
import sys
import time

class Gather():
    
    def __init__(self, consumerKey,consumerSecret,accessToken,accessTokenSecret,
                 option = None, totalSize = 100, fileSize = 100):
        #initialize the gathering engine
        global total_size
        total_size = totalSize
        global file_size
        file_size = fileSize
        
        global consumer_key
        consumer_key = consumerKey
        global consumer_secret
        consumer_secret = consumerSecret
        global access_token
        access_token = accessToken
        global access_token_secret
        access_token_secret = accessTokenSecret
        
        if (os.path.isfile('simile2.smile'))==False:
            print('oauth_dance')
            token,token_key = oauth_dance('The Insight Project',consumer_key,consumer_secret,token_filename='simile2.smile')
            #print('oauth_consumer_key='+token_key)
            #print('oauth_token       ='+token)
            with open('simile2.smile','r') as f:
                token2 = f.readline()[:-1]
                token_key2 = f.readline()[:-1]
                #print('oauth_consumer_key='+token_key2)
                #print('oauth_token       ='+token2)
            f.close()
        else:
            with open('simile2.smile','r') as f:
                token = f.readline()[:-1]
                token_key = f.readline()[:-1]
        global twitter_object
        twitter_object = Twitter(auth=OAuth(token, token_key, 
                                            consumer_key, consumer_secret))
        twitter_object.search.tweets(q='test')
        global twitter_stream
        twitter_stream = TwitterStream(auth=OAuth(token, token_key, 
                                            consumer_secret, consumer_key))
        global setting
        setting = 0
        if option == 'happy':
            #search happy tweets
            setting = 1
        elif option == 'sad':
            #search sad tweets
            setting = -1
        else:
            #search random tweets
            setting = 0
    
    def run(self, start_index=1):
        #do a collection run
        try:
            t = twitter_object
            search_level = 0
            if(setting == 1):
                #happy
                print(str(search_level+1)+" Happy Search!")
                search_result = t.search.tweets(q=':)',
                                                lang='en',
                                                count=min(100,total_size),
                                                include_entities=False,
                                                result_type = 'recent')
                search_level = search_level + 1
            elif(setting == -1):
                #sad
                print("sad search :(")
                search_result = t.search.tweets(q=':(',
                                                lang='en',
                                                count=min(100,total_size),
                                                include_entities=False,
                                                result_type = 'recent')
                search_level = search_level + 1
            else:
                print("Search.")
                search_result = t.search.tweets(q='-organogenesis',
                                                lang='en',
                                                count=min(100,total_size),
                                                include_entities=False,
                                                result_type = 'recent')
                search_level = search_level + 1
            s = search_result
            #print(s['search_metadata'])
            
            
            # write from here to raw files
            #print('search_result[0]:')
            #print('tweet:'+s['statuses'][0]['text'].encode('utf-8'))
            error_count = 0
            count = 0
            search_count = 0
            #print('file count = '+str(int(ceil(total_size/file_size))))
            for index in range(start_index,int(ceil(total_size/file_size))+start_index):
                file_name = ''
                if(setting ==1):
                    file_name = file_name+'happy'
                elif(setting==-1):
                    file_name = file_name+'sad'
                else:
                    file_name = file_name+'gen'
                index_string = '0000'+str(index)
                index_string = index_string[-4:]
                full_file = r'/home/buck/Github/Insight/statistics/raw/'+file_name+index_string+r'.txt'
                #print('count = '+str(count)+' vs. len()'+str(len(search_result['statuses']))+' for file '+str(index))
                with open(full_file,'w') as f:
                    for i in range(0,file_size):
                        try:
                            if(search_count >= len(search_result['statuses'])):
                                break
                            #print(str(count+1)+' -> '+search_result['statuses'][count]['text'].encode('utf-8'))
                            f.write(s['statuses'][search_count]['text'].encode('utf-8')+'\n')
                            count = count +1
                            search_count = search_count +1
                        except Exception as e:
                            error_count = error_count+1
                            count = count +1
                            search_count = search_count+1
                            print(e)
                if(count < total_size and search_count >= len(s['statuses'])):
                    search_count = 0
                    if(setting == 1):
                        #happy
                        print(str(search_level+1)+" Happy Search!")
                        search_result = t.search.tweets(q=':)',
                                                        lang='en',
                                                        count=min(100,total_size),
                                                        include_entities=False,
                                                        result_type = 'recent')
                        search_level = search_level + 1
                    elif(setting == -1):
                        #sad
                        print("sad search :(")
                        search_result = t.search.tweets(q=':(',
                                                        lang='en',
                                                        count=min(100,total_size),
                                                        include_entities=False,
                                                        result_type = 'recent')
                        search_level = search_level + 1
                    else:
                        print("Search.")
                        search_result = t.search.tweets(q='-organogenesis',
                                                        lang='en',
                                                        count=min(100,total_size),
                                                        include_entities=False,
                                                        result_type = 'recent')
                        search_level = search_level + 1
                    s = search_result
            print('done!')
        except TwitterHTTPError as rate_limit:
            print(rate_limit)
            print('\n --> Sleeping for 15 min to ensure rate limit is clear')
            time.sleep(60*15)
            print('\n Sleep complete -->')
            
        
        
def test():
    f = open(r'/home/buck/Github/Insight/statistics/simile.smile','r')
    total_size = input('total size: ')
    file_size = input('file size: ')
    index_num = input('beginning input for gather write, pretty please: ')
    g = Gather(option='happy',totalSize = total_size, fileSize = file_size,
                     consumerKey = f.readline()[:-1], consumerSecret = f.readline()[:-1],
                     accessToken = f.readline()[:-1], accessTokenSecret = f.readline())
    g.run(index_num)
    print('end in main run')
    sys.exit(0)

if __name__ == '__main__':
    print('test Gather')
    test()
    print('end test Gather')