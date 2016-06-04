from flask import render_template

from app import server


@server.route('/')
@server.route('/index')
def index():
    user = {'nickname': 'Buck'}  # fake user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'Avengers!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@server.route('/fast')
def fast():
    return "f"
