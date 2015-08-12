from web_app.app import app
from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_user, logout_user
from web_app.app.forms import LoginForm, SignupForm
from web_app.app import db
from web_app.app.models import User


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'fakeBuck'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user, 
                           posts=posts)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(t_screen_name=form.username.data).first()  # @UndefinedVariable
        flash('Login requested for Username="%s"' % (form.username.data))
        if(user and user.check_password(form.password.data)):
            login_user(user, form.remember_me.data)
            return redirect('/index')
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash('Signup requested for username="%s", remember_me=%s' % (form.username.data))
        if(form.password.data == form.confirm_password.data):
            # Signup user
#             new_user = User('username','password')
#             db.session.add(new_user)
#             db.session.commit
            # login_user(user, form.remember_me.data)
            pass
    flash('The site is not accepting users right now, unfortunately')
    return redirect('/index')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), 500