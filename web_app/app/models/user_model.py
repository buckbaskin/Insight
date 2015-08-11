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