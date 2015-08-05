from web_app.config import secret_config

config = dict([('DEBUG', True), 
               ('PORT', 5000), 
               ('HOST', '127.0.0.1'),
               ('WTF_CSRF_ENABLED', True),
               ('OPENID_PROVIDERS', [{'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
                                    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
                                    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
                                    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
                                    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]),
               ('SECRET_KEY', secret_config.SECRET_KEY)])
