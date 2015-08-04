from TwitterSearch import *
import os
import collections

class TwitterSearchInterface:
    def __init__(self,consumerKey,consumerSecret,accessToken,accessTokenSecret,output_file_base="",output_count=1):
        global consumer_key
        consumer_key = consumerKey
        global consumer_secret
        consumer_secret = consumerSecret
        global access_token
        access_token = accessToken
        global access_token_secret
        access_token_secret = accessTokenSecret
        global order
        order = TwitterSearchOrder()
        global output_base
        output_base = output_file_base
        global output_num
        output_num = output_count
    
    def query(self,complete_input):
        try:
#            print('keywords: '+str(complete_input.keywords))
#            print('mods    : '+str(complete_input.modifiers))
#            print('mods[2] : '+str(False == complete_input.modifiers[2]))
            order.setKeywords(complete_input.keywords) # keywords to search for
            order.setLanguage(complete_input.modifiers[0]) # language for tweets
            order.setCount(complete_input.modifiers[1]) # result count
            order.setIncludeEntities(complete_input.modifiers[2]) # extra info?
            
            # it's about time to create a TwitterSearch object with our secret tokens
#            print('ck: '+str(consumer_key)[:-1]+
#                  '\ncs: '+consumer_secret[:-1]+
#                  '\nat: '+access_token[:-1]+
#                  '\nass: '+access_token_secret[:]+
#                  '\nend')
            ts = TwitterSearch(
                               consumer_key = consumer_key,
                               consumer_secret = consumer_secret,
                               access_token = access_token,
                               access_token_secret = access_token_secret
                               )
            error_count = 0
            #print('meta: '+ts.getMetadata()+'\n--end meta')
            search = ts.searchTweetsIterable(order)
            for index in range(0,output_num):
                file_index = ('0000'+str((index+1)))
                file_index = file_index[len(file_index)-4:]
                file_mod = '_'
                for word in complete_input.keywords:
                    file_mod = file_mod+str(word)+'_'
                print('replace1: '+file_mod)
                file_mod.replace("#", '.HASH.')
                file_mod.replace("@", '.AT.')
                print('replace2: '+file_mod)
                #print("file_mod: "+file_mod)
                with open(r'/home/buck/Github/Insight/data_collection/output/'+
                          output_base+file_mod+file_index+'.txt','w') as f:
                    for count in range(0,20):
                        try:
                            tweet = search.next()
                            s = '<u>%s<><t>%s<>\n' % ( tweet['user']['screen_name'], tweet['text'] )
                            f.write(s.encode('utf8'))
                        except Exception as e:
                            error_count = error_count+1
                            print(e)
#                print('file_path: '+os.path.abspath(f.name))
                f.close()
            print('Report:')
            print('Errors: '+str(error_count))
            return True
                
        except TwitterSearchException as e: # take care of all those ugly errors if there are some
            print('TwitterSearchExceptionError -> '+str(e))
            return False
    
    
    def setModifiers(self,language='en',count='100',entities=False):
        mod_list = list()
        mod_list.append(language)
        mod_list.append(count)
        mod_list.append(entities)
        return mod_list
    
    def get_input(self):
        #parse keyword input by splitting on the commas
        unparsed_input = raw_input('Please choose search keywords: ')
        parsed_input = unparsed_input.split(',')
        mod_input = raw_input('[language str],[count #],[extra info?] : ')
        mod_split = mod_input.split(',')
        mods = self.setModifiers('en', eval(mod_split[1]), eval(mod_split[2]))
        #print('[0] '+str(mod_split[0]=='en')+' [1] '+str(eval(mod_split[1])==10)+' [2] '+str(eval(mod_split[2])==False))
        input_set = collections.namedtuple('input', ['keywords','modifiers'])
        complete_input = input_set(parsed_input,mods)
        return complete_input
    
    