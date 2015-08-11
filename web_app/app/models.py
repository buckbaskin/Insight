from web_app.app import db
from web_app.app.models.user_model import User
from web_app.app.models.twitter_model import Follows, Status, Hashtag, Tags
    
class Post(db.Model):
    # This is a post from the tutorial
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)