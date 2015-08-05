from web_app.app import app

@app.route('/')
@app.route('/index')

def index():
    return "Hello, World!"