from app import db
# from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

from sqlalchemy.dialects.postgresql import JSON

import datetime

# MANY TO MANY TABLES

# example many to many relationship #manytomany
followers = db.Table('followers',
                         db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )
hashtags = db.Table('hashtags',
                         db.Column('status_id', db.Integer, db.ForeignKey('status.id')),
                         db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id'))
                     )

class User(db.Model):
    
    def __init__(self, username):
        self.t_screen_name = username
        self.last_updated = datetime.datetime.utcnow()
        self.description = ''
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Site Info
    
    # tracking = db.Column(db.Boolean)
    last_updated = db.Column(db.DateTime)
    
    # Twitter Info
    
    t_screen_name = db.Column(db.String(120), index=True, unique=True)
    statuses = db.relationship('Status', backref='author', lazy='dynamic')
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
        if isinstance(user, int):
            return self.followed.filter(followers.c.followed_id == user).count() > 0
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
    
    # Twitter Info
    hashtags = db.relationship('Hashtag',
                               secondary=hashtags,
                               primaryjoin=(hashtags.c.status_id == id),
                               secondaryjoin=(hashtags.c.hashtag_id == id),
                               backref=db.backref('statuses', lazy='dynamic'),
                               lazy = 'dynamic')
#     mentions = db.relationship('User',
#                                secondary=mention,
#                                primaryjoin=(mention.c.user_id == id),
#                                secondaryjoin=(mention.c.status_id == id),
#                                backref=db.backref('followers', lazy='dynamic'),
#                                lazy = 'dynamic')
    # in_reply_to = db.Column(db.Integer, db.ForeignKey('status.id'))
    t_id = db.Column(db.Integer)
    text = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Hashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, index = True)
    
class Trace(db.Model):
    #trace created on first load (w/o trace), passed between pages as they are loaded
     
    def __init__(self):
        self.start = datetime.datetime.utcnow()
     
    def __repr__(self):
        return '<Trace %s>' % (str(self.id),)
     
    def serialize(self):
        return self.id
     
    @staticmethod
    def deserialize(num):
        # id_num = int(string[8:])
        ses = Trace.query.get(num)
        if ses is None:
            ses = Trace()
            db.session.add(ses)
            db.session.commit()
        return ses
     
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    pages = db.relationship('PageLoad', backref='trace', lazy='dynamic')
    
    def avatar(self, size):
        return ('http://www.gravatar.com/avatar/%s?d=retro&s=%d' %
                (md5(str(self.id).encode('utf-8')).hexdigest(), size))
     
class PageLoad(db.Model):
     
    def __init__(self, trace, page_name):
        self.time = datetime.datetime.utcnow()
        if isinstance(trace, int):
            self.trace_id = trace
        else:
            self.trace_id = trace.id
        self.page_id = page_name
         
    def __repr__(self):
        return '<PageLoad %s>' % (str(self.page_id),)
    
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    page_id = db.Column(db.String(80))
    trace_id = db.Column(db.Integer, db.ForeignKey('trace.id'))
    
    def avatar(self, size):
        return ('http://www.gravatar.com/avatar/%s?d=retro&s=%d' %
                (md5(str(self.page_id).encode('utf-8')).hexdigest(), size))
        
# class Result(db.Model):
#     __tablename__ = 'results'
#     
#     id = db.Column(db.Integer, primary_key=True)
#     url = db.Column(db.String())
#     result_all = db.Column(JSON)
#     result_no_stop_words = db.Column(JSON)
# 
#     def __init__(self, url, result_all, result_no_stop_words):
#         self.url = url
#         self.result_all = result_all
#         self.result_no_stop_words = result_no_stop_words
# 
#     def __repr__(self):
#         return '<Result: id {}>'.format(self.id)

class FollowTree(db.Model):
    
    def __init__(self, t_screen_name):
        self.last_updated = datetime.datetime.utcnow()
    
    def __repr__(self):
        return '<FollowTree %s>' % (str(self.user_id))
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_updated = db.Column(db.DateTime)
    
class FollowTreeNode(db.Model):
    
    def __init__(self, tree, parent=None, user):
        self.tree = tree.id
        if parent:
            self.parent = parent.id
        self.user_id = user.id
    
    def __repr__(self):
        return '<FollowNode %s>' % (str(self.id))
    
    id = db.Column(db.Integer, primary_key=True)
    tree = db.Column(db.Integer, db.ForeignKey('followtree.id'))
    parent = db.Column(db.Integer, db.ForeignKey('followtreenode.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def is_following(self, user):
        # TODO(buckbaskin): implement by getting user, calling is_following method
        return False