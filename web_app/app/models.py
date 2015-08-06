from web_app.app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_screen_name = db.Column(db.String(120), index=True, unique=True)
    
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
        return '<User %r>' % (self.nickname)
    
class Follows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.Integer, db.ForeignKey('user.t_userame'), index=True)
    followee = db.Column(db.Integer, db.ForeignKey('user.t_userame'), index=True)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
    
