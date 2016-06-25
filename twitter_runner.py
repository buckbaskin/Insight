from Insight.twitter_api.tasks import get_followers_test, screen_name_to_id

for user in screen_name_to_id(['beBaskin']):
    print(user)


get_followers_test(next(screen_name_to_id(['beBaskin'])))
