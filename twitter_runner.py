from Insight.twitter_api.tasks import get_followers_test, screen_name_to_id, max_rate_limit

print(max_rate_limit())

for user in screen_name_to_id(['beBaskin']):
    print(user)

get_followers_test(next(screen_name_to_id(['beBaskin'])))

print(max_rate_limit())
