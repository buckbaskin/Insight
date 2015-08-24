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
        print 'I found an avatar!!! for johnDoe, 128'+str(avatar)
        expected = 'http://www.gravatar.com/avatar/idkwhattoputhere'
        assert avatar[0:len(expected)] == expected
        
if __name__ == '__main__':
    unittest.main()