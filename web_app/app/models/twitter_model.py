from web_app.app import db

class Follows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.Integer, db.ForeignKey('user.t_userame'), index=True)
    followee = db.Column(db.Integer, db.ForeignKey('user.t_userame'), index=True)
    
class Status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    favorited = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    
class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey(''))
    
class Hashtag(db.Model):
    text = db.Column(db.String, primary_key = True)