from twitter import *
import os
import collections

class PTTInterface():

    def __init__(self,consumerKey,consumerSecret,accessToken,accessTokenSecret,
                 output_file_base="",num_output_files=1,len_output_files=20):
        global consumer_key
        consumer_key = consumerKey
        global consumer_secret
        consumer_secret = consumerSecret
        global access_token
        access_token = accessToken
        global access_token_secret
        access_token_secret = accessTokenSecret
        
        global output_base
        output_base = output_file_base
        global output_count
        output_count = num_output_files
        global output_length
        output_length = len_output_files
        
        
        if (os.path.isfile('simile2.smile'))==False or True:
            print('oauth_dance')
            token,token_key = oauth_dance('The Insight Project',consumer_key,consumer_secret,token_filename='simile2.smile')
        else:
            with open('simile2.smile','r') as f:
                token = f.readline()[:-1]
                token_key = f.readline()
        global twitter_object
        twitter_object = Twitter(auth=OAuth(token, token_key, 
                                            consumer_key, consumer_secret))
        twitter_object.search.tweets(q='test')
        global twitter_stream
        twitter_stream = TwitterStream(auth=OAuth(token, token_key, 
                                            consumer_secret, consumer_key))
        
    def search(self,query,                              #query
               language='en',result_type='recent',      #tweet modifiers
               extra_info=False,                        #results modifiers
               num_output_files=1,len_output_files=20   #output modifiers
               ):
        t = twitter_object
        try:
            search_result = t.search.tweets(q=query,
                                            lang='en',
                                            count=min(100,num_output_files*len_output_files),
                                            include_entities=False,
                                            result_type = 'recent')
        except Exception as e:
            print(str(e))
            
        print('search_result[0]:')
        print('user :'+search_result['statuses'][0]['user']['screen_name'])
        print('tweet:'+search_result['statuses'][0]['text'].encode('utf-8'))
        print(':end results')
        error_count = 0
        count = 0
        for index in range(0,output_count):
            file_index = ('0000'+str((index+1)))
            file_index = file_index[len(file_index)-4:]
            file_mod = query
            print('replace1: '+file_mod)
            file_mod.replace("#", '.HASH.')
            file_mod.replace("@", '.AT.')
            file_mod.replace(" ", "_")
            print('replace2: '+file_mod)
            full_file = r'/home/buck/Github/Insight/data_collection/output/'+output_base+file_mod+file_index+'.txt'
            with open(r'/home/buck/Github/Insight/data_collection/output/'+
                      output_base+file_mod+file_index+'.txt','w') as f:
                for i in range(0,output_length):
                    try:
                        if(count >= len(search_result['statuses'])):
                            break
                        print(str(count)+' -> '+search_result['statuses'][count]['user']['screen_name'].encode('utf-8')+' tweeted '+search_result['statuses'][count]['text'].encode('utf-8'))
                        s = '<u>'+search_result['statuses'][count]['user']['screen_name'].encode('utf-8')+'<><t>'+search_result['statuses'][count]['text'].encode('utf-8')+'<>\n'
                        s.replace('&amp;','&')
                        f.write(s.encode('utf8'))
                        count = count +1
                    except Exception as e:
                        error_count = error_count+1
                        count = count +1
                        print(e)
#            print('file_path: '+os.path.abspath(f.name))
            if(count >= len(search_result['statuses'])):
                break
            f.close()
        print('Report:')
        print('Errors: '+str(error_count))
        return full_file
    
    def stream(self, keywords,tags=list(),users=list()):
        pass
    
    def user_search(self,q):
        t = twitter_object
        search_result = t.users.search(q=q,lang='en')
        for user in range(0,len(search_result)):
            print('user '+str(user+1)+' -> '+search_result[user]['name'].encode('utf-8')+' ('+search_result[user]['id_str'].encode('utf-8')+')')
    
    
    