from flask.ext.wtf import Form
from flask import flash
from wtforms import StringField # , BooleanField, PasswordField
from wtforms.validators import DataRequired, Length
from wtforms.fields.simple import TextAreaField
from web_app.app.models import User

class EditForm(Form):
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    
    def validate(self):
        return True

# class LoginForm(Form):
#     username = StringField('twitter username', validators=[DataRequired()])
#     password = PasswordField('password', validators=[Length(min=8, max=30)])
#     remember_me = BooleanField('remember_me', default=False)

class SignupForm(Form):
    username = StringField('twitter username', validators=[DataRequired()])
    
    def validate(self):
        if not Form.validate(self):
            return False
        conflict = User.query.filter_by(t_screen_name=self.username.data).first() # @UndefinedVariable
        if conflict != None:
            flash('Username already in db')
        return conflict == None
    
class PostForm(Form):
    post = StringField('post', validators=[DataRequired(), Length(min=0, max=140)])
    
class ReqForm(Form):
    url = StringField('url', validators=[DataRequired()])