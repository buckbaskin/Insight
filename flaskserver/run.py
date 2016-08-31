#!venv/bin/python3
import subprocess

from app import server

subprocess.Popen('python3 run_service.py', shell=True)
print('running main server now')
server.config['SERVER_NAME'] = '127.0.0.1:5000'
server.run(debug=True, use_reloader=True)

