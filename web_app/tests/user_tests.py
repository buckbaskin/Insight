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
        
if __name__ == '__main__':
    unittest.main()