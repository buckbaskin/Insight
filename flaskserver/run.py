#!venv/bin/python3
import subprocess

from app import server

server.config['SERVER_NAME'] = '127.0.0.1:5000'
server.run(debug=True, use_reloader=True)

