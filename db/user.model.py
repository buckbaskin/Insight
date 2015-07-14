from mongothon import Schema, Mixed, Array
from dbus.exceptions import ValidationException

class SchemaGenerator(object):
    def __init__(self):
        self.tweet_schema = Schema({
                                    "created": {"type":datetime }
                                    ,"favorite_count": {"type":int }
                                    ,"favorited": {"type": boolean }
                                    ,"filter": {"type":basestring, "validates": one_of("none", "low", "medium", "high") }
                                    ,"t_id": {"type":int}
                                    ,"replied_to_by_id": {"type":int}
                                    ,"retweet_count": {"type":int}
                                    ,"text": {"type":basestring, "required": True }
                                    })
        self.user_schema = Schema({
                              ### TWITTER PROFILE INFORMATION
                              # identifying information
                              "t_user_id": {"type":int, "required": True}
                              ,"full_user": {"type":boolean, "required":True}
                              
                              # hydrated user content from https://api.twitter.com/1.1/users/show.json
                              #      in bulk: https://api.twitter.com/1.1/users/lookup.json
                              ,"t_screen_name": {"type": basestring}
                              ,"name": {"type": basestring}
                              ,"created": {"type":datetime }
                              ,"description": {"type": basestring }
                              ,"following": {"type":boolean}
                              ,"friend_count": {"type":int}
                              
                              # separate request https://api.twitter.com/1.1/friends/ids.json
                              ,"following_by_id": {type:Array(int)}
                              # separate request https://api.twitter.com/1.1/followers/ids.json
                              ,"followers_by_id": {type:Array(int)}
                              
                              # statuses request https://api.twitter.com/1.1/statuses/user_timeline.json
                              ,"tweets": {type:Array(self.tweet_schema)}
                              })
        self.model = create_model(self.user_schema, db[collection])
        
    def user_schema(self):
        return self.user_schema
    
    def user_model(self):
        return self.model
        
    def init_user(self, t_user_id, db, collection):
        user = (user_model())({
                               "t_user_id": t_user_id
                               ,"full_user": True
                               })
        try:
            user.validate()
            user.save()
            return user
        except ValidationException:
            pass
        return None
    
    def fill_user(self, t_user_id, screen_name, name, created, description, following, friend_count):
        user = User.find_one({'t_user_id': t_user_id})
        if user is None:
            return None
        if screen_name is not None:
            user['screen_name'] = screen_name
        if name is not None:
            user['name'] = name
        if created is not None:
            user['created'] = created
        if description is not None:
            user['description'] = description
        if following is not None:
            user['following'] = following
        if friend_count is not None:
            user['friend_count'] = friend_count
        
        
    