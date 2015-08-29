#!/usr/bin/env python
import sys
# print 'sys_path:'
# print sys.path
# sys.path[0] = '/home/pi/Insight'
sys.path.append('/home/pi/Insight')
# print 'sys_path 2:'
# print sys.path
from web_app.app import app
from web_app.config import server_config

# === APP ===

app.config.from_object(server_config)
app.run(host='0.0.0.0', port=80)
