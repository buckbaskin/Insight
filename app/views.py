from app import server

@server.route('/')
@server.route('/index')
def index():
    return "Hello, World!"

@server.route('/fast')
def fast():
    return "f"

