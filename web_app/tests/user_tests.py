import os
import unittest

from web_app.config.server_config import basedir
from web_app.app import app, db
from web_app.app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_avatar(self):
        u = User('johnDoe')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/9a0c75a27f67d0496095d060f28fb8ed'
        assert avatar[0:len(expected)] == expected
        
    def test_follow(self):
        u1 = User('john')
        u2 = User('susan')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) is None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().t_screen_name == 'susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().t_screen_name == 'john'
        u = u1.unfollow(u2)
        assert u is not None
        db.session.add(u)
        db.session.commit()
        assert not u1.is_following(u2)
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0
        
if __name__ == '__main__':
    unittest.main()