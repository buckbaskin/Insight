from web_app.app import db
# from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    
    def __init__(self, username):
        self.t_screen_name = username
    
    id = db.Column(db.Integer, primary_key=True)
    t_screen_name = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    contributors = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(True))
    description = db.Column(db.String(400))
    favourites_count = db.Column(db.Integer)
    followers_count = db.Column(db.Integer)
    following = db.Column(db.Boolean)
    friends_count = db.Column(db.Integer)
    t_id = db.Column(db.Integer)
    name = db.Column(db.String(30))
    statuses_count = db.Column(db.Integer)
    verified = db.Column(db.Boolean)

    def __repr__(self):
        return '<User %r>' % (self.t_screen_name)
    # Git anchor
    
    # Git anchor
    # user login model
    # Git anchor
    
#     @staticmethod
#     def make_unique_nickname(nickname):
#         if User.query.filter_by(nickname=nickname).first() is None:
#             return nickname
#         version = 2
#         while True:
#             new_nickname = nickname + str(version)
#             if User.query.filter_by(nickname=nickname).first() is None:
#                 break
#             version += 1
#         return new_nickname
    
class Follows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.Integer, db.ForeignKey('user.t_screen_name'), index=True)
    followee = db.Column(db.Integer, db.ForeignKey('user.t_screen_name'), index=True)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
    
class Status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    favorited = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    
class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey(''))
    
class Hashtag(db.Model):
    text = db.Column(db.String, primary_key = True)