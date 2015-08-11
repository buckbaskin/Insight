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
    
    # Git anchor
    # user login model
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    # Git anchor
    
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=nickname).first() is None:
                break
            version += 1
        return new_nickname
    
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
    
class Status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    favorited = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    
class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey(''))
    
class Hashtag(db.Model):
    text = db.Column(db.String, primary_key = True)