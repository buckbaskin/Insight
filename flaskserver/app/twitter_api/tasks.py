import collections
import datetime
import os
import time
from twitter.api import TwitterHTTPError
from app.twitter_api.api import TwitterAccess, TwitterAccessMock

from app.wishlist import FileNotFoundError # 2->3 shim

try:
    api = TwitterAccess().start().api
except (FileNotFoundError,  IOError,):
    api = TwitterAccessMock().start().api

def max_rate_limit(output=False):
    min_remaining = 180
    expiration_time = None
    if output:
        print('rate limit things')
    result = api.application.rate_limit_status()['resources']
    for context in result:
        if output:
            print('context %s' % (context,))
        for endpoint in result[context]:
            endpoint = result[context][endpoint]
            if output:
                print('remaining: limit %d remaining %d reset %d' % (endpoint['limit'], endpoint['remaining'], endpoint['reset'],))
            if endpoint['remaining'] < min_remaining:
                min_remaining = endpoint['remaining']
                expiration_time = endpoint['reset']
            if endpoint['remaining'] == 0 and min_remaining == 0:
                if expiration_time < endpoint['reset']:
                    expiration_time = endpoint['reset']
    return (min_remaining, expiration_time,)

def handle_rate_error(err):
    print('You are probably getting rate limited.')
    # print(err)
    reset_time = max_rate_limit()[1]
    current_time = (datetime.datetime.now() - datetime.datetime.utcfromtimestamp(0)).total_seconds()
    print('sleep %d seconds '% (int(reset_time - current_time) - 4*60*60,))
    time.sleep(int(reset_time - current_time) - 4*60*60)

def screen_name_to_id(screen_name):
    if isinstance(screen_name, collections.Iterable):
        result = api.users.lookup(screen_name=','.join(screen_name), include_entities=False)
        new_result = []
        for user in result:
            new_result.append(user['id'])
    else:
        result = api.users.lookup(screen_name=[screen_name])
        new_result = []
        for user in result:
            new_result.append(user['id'])

    return new_result


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
        return sorted(iterable, key=condition)

    count = 0
    return list(sort_generator(get_followers(user_id), lambda user: user['followers_count']))
    # for user in sort_generator(get_followers(user_id), lambda user: user['followers_count']):
    #     count += 1
    #     print('%d %s has %d followers' % (count, user['name'], user['followers_count']))


