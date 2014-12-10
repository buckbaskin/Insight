from data_collection.PTTRunner import Runner

class Regression():
    
    def __init__(self):
        global x_var #x variables to test
        x_var = []
        global x_cor #correlations for x_var
        x_cor = []
    
    def _y_(self,dependent_variable):
        global y_var
        y_var = dependent_variable
        # test how well this variable is indicated by x variables
    
    def add_x(self,test_variable):
        global x_var
        x_var.append(test_variable)
    
    def clear_x(self):
        global x_var
        x_var = []
        global x_cor
        x_cor = []
    
    def collect_data(self, n=10,trials=1,test_id='000'):
        Runner('y_'+y_var.id_str+test_id)
        

class TwitterVariable():
    def __init__(self,string_representation, other_data_string=None):
        global id_str
        id_str = string_representation
        if string_representation == 'followers':
            global test_var
            test_var = 100
        elif string_representation == 'follows':
            global test_var
            test_var = 101
        elif string_representation == '#perTweet':
            global test_var
            test_var = 102
        elif string_representation == '@perTweet':
            global test_var
            test_var = 103
        elif string_representation == 'retweetRate':
            global test_var
            test_var = 104
        elif string_representation == 't-content':
            global test_var
            test_var = 106
            if other_data_string != None:
                global extra
                extra = other_data_string
            else:
                global test_var
                test_var = -1
        elif string_representation == 'replyRate':
            global test_var
            test_var = 108
        elif string_representation == 'postCount':
            global test_var
            test_var = 110
        elif string_representation == 'postRate':
            global test_var
            test_var = 111
        elif string_representation == 'd-content':
            global test_var
            test_var = 113
            if other_data_string != None:
                global extra
                extra = other_data_string
            else:
                global test_var
                test_var = -1
        else:
            global test_var
            test_var = -1
        
    ''' Variable Reference 
    
    by user
    -100    followers - popularity
    -101    follows - connections
    -102    # per tweet (avg. per user)
    -103    @ per tweet
    -104    average tweet retweet time per time of day (estimate of time spent on twitter)
    105    common tweet time (of day)
    -106*  tweet content (key words for a user?)
    107    twitter app (Web, Android, Iphone, Ipad) %use?
    bool    language (en)
    -108    % reply to users? - percent of tweets that are replying to other users
    bool    verified?
    na    geolocation?
    109    utc offset - approximate location
    -110    status count - user posts
    -111        status rate (status count / time on twitter)
    112    friends count - user friends with others
    -113*    description content (key words?)
    114    favorites count - user favorites others
    
    * for this information, the frequency of the given search term(s) are used as a more specific metric
    
    by tweet
    201    # per tweet (point estimator for user)
    202    @ per tweet (point estimator for user)
    203    retweet time (point estimator) no retweet = skip
    204    favorite count
    205*    tweet content (key words among all tweets?)
    206    twitter app of choice
    207    utc offset
    
    '''