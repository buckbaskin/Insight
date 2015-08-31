from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

import sys
sys.path.append('/home/buck/Github/Insight')
from web_app.app import app, db
from web_app.config import server_config

app.config.from_object(server_config)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()