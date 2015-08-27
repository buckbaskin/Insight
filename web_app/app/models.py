from web_app.app import db
# from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

import datetime

# MANY TO MANY TABLES

# example many to many relationship #manytomany
followers = db.Table('followers',
                         db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )

class User(db.Model):
    
    def __init__(self, username):
        self.t_screen_name = username
        self.last_updated = datetime.datetime.utcnow()
        self.description = ''
    
    id = db.Column(db.Integer, primary_key=True)
    t_screen_name = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    last_updated = db.Column(db.DateTime)
    
    contributors = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(True))
    description = db.Column(db.String(400))
    favourites_count = db.Column(db.Integer)
    followers_count = db.Column(db.Integer)
    friends_count = db.Column(db.Integer)
    t_id = db.Column(db.Integer)
    name = db.Column(db.String(30))
    statuses_count = db.Column(db.Integer)
    verified = db.Column(db.Boolean)
    
    profile_url = db.Column(db.String(100))
    
    # example many to many relationship #manytomany
    '''
    column = db.relationship( right side of relationship (left side is parent class),
                                secondary = association table for relationship
                                primaryjoin = condition that links left side with association
                                secondaryjoin = condition that links the right side with association
                                backref = how relationship is accessed from right side entity
                                dynamic means run when specificially requested, more later?
                                )
    '''
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy = 'dynamic')


    def __repr__(self):
        return '<User %r>' % (self.t_screen_name)
    # Git anchor
    
    def avatar(self, size):
        self.onPageLoad()
        if self.profile_url:
            return str(self.profile_url)
        return ('http://www.gravatar.com/avatar/%s?d=retro&s=%d' %
                (md5(self.t_screen_name.encode('utf-8')).hexdigest(), size))
        
    def onPageLoad(self):
        if self.last_updated == None:
            self.last_updated = datetime.datetime.utcnow()
            db.session.add(self)
            db.session.commit()
        
        # add user posts to their stream
        self.follow(self)
            
    # Git anchor

    # managing edges in many to many relationship #manytomany
    def follow(self, user):
        # if parent is not following user, follow user
        if not self.is_following(user):
            self.followed.append(user)
            return self
        
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
        
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        '''
        join: create new extended table of posts, 
                where any post (Post) 
                that is by a user that is followed (followers.c.followed_id == Post.user_id) 
                has the follow relationship appended (followers)
        filter: refine the above table to only include posts that are followed by this (parent) user (followers.c.follwer_id == self.id)
                Note: result will be posts without appended filter information
        order_by: ordered by the time stamp column (Post.timestamp.desc())
        '''
        # Note returns a query
        return (Post.query.join(followers, (followers.c.followed_id == Post.user_id))
                            .filter(followers.c.follower_id == self.id)
                            .order_by(Post.timestamp.desc()))
    
    # Git anchor
    
# class Follows(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     follower = db.Column(db.Integer, db.ForeignKey('user.t_screen_name'), index=True)
#     followee = db.Column(db.Integer, db.ForeignKey('user.t_screen_name'), index=True)
    
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
    status = db.Column(db.Integer, db.ForeignKey('status.id'))
    
class Hashtag(db.Model):
    text = db.Column(db.String, primary_key = True)
    
class Session(db.Model):
    #session created on homepage load (w/o session), passed between pages as they are loaded
    
    def __init__(self):
        self.start = datetime.datetime.utcnow()
    
    def __repr__(self):
        return '<Session %s>' % (str(self.t_screen_name),)
    
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    pages = db.relationship('PageLoad', backref='session', lazy='dynamic')
    #posts = db.relationship('Post', backref='author', lazy='dynamic')
    
class PageLoad(db.Model):
    
    def __init__(self, session, page_name):
        self.time = datetime.datetime.utcnow()
        self.session = session
        self.page_id = page_name
        
    def __repr__(self):
        return '<PageLoad %s>' % (str(self.page_id),)
    
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    page_id = db.Column(db.String(80))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))