#!venv/bin/python
from Insight.service import server

server.config['SERVER_NAME'] = '127.0.0.1:5001'
server.run(debug=True, use_reloader=True)