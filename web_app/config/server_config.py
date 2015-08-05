from web_app.config import secret_config

config = dict([('DEBUG', True), 
               ('PORT', 5000), 
               ('HOST', '127.0.0.1'),
               ('WTF_CSRF_ENABLED', True),
               ('SECRET_KEY', secret_config.SECRET_KEY)])
