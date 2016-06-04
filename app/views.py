from app import server


@server.route('/')
@server.route('/index')
def index():
    user = {'nickname': 'Buck'}  # fake user
    return render_template('index.html',
       title='Home',
                           user=user)


@server.route('/fast')
def fast():
    return "f"
