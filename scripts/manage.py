from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

import sys
if not '/home/buck/Github/Insight' in sys.path:
    sys.path.append('/home/buck/Github/Insight')
print 'manage.py: '
print sys.path

from app import server, db
from config import server_config

server.config.from_object(server_config)

migrate = Migrate(server, db)
manager = Manager(server)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
