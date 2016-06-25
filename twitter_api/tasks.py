import collections
import time
from twitter.api import TwitterHTTPError
from Insight.twitter_api.api import TwitterAccess

api = TwitterAccess().api

def handle_rate_error(err):
    time.sleep(60)

def screen_name_to_id(screen_name):
    if isinstance(screen_name, collections.Iterable):
        result = api.users.lookup(screen_name=','.join(screen_name), include_entities=False)
        for user in result:
            yield user['id']
    else:
        result = api.users.lookup(screen_name=[screen_name])
        for user in result:
            yield user['id']


def get_followers(user_id):
    try:
        cursor = -1
        last_cursor = 0
        while(True):
            print('API.FOLLOWERS.IDS()')
            follows = api.followers.list(user_id=str(user_id), count=200, cursor=-1)
            for follower in follows['users']:
                yield follower
            
            print('%d %d' % (follows['next_cursor'], follows['previous_cursor'],))
            if follows['previous_cursor'] == follows['next_cursor']:
                break
            else:
                cursor = follows['next_cursor']

    except TwitterHTTPError as the:
        handle_rate_error(the)

def get_followers_test(user_id):
    def sort_generator(iterable, condition):
        for item in  sorted(iterable, key=condition):
            yield item

    count = 0
    for user in sort_generator(get_followers(user_id), lambda user: user['followers_count']):
        count += 1
        print('%d %s has %d followers' % (count, user['name'], user['followers_count']))
