from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length
from wtforms.fields.simple import TextAreaField
from web_app.app.models import User

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    
    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname
    
    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()  # @UndefinedVariable
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True

# class LoginForm(Form):
#     username = StringField('twitter username', validators=[DataRequired()])
#     password = PasswordField('password', validators=[Length(min=8, max=30)])
#     remember_me = BooleanField('remember_me', default=False)
#     
# class SignupForm(Form):
#     username = StringField('twitter username', validators=[DataRequired()])
#     password = PasswordField('password (not from twitter)', validators=[Length(min=8, max=30)])
#     confirm_password = PasswordField('Confirm password', validators=[Length(min=8, max=30)])
#     remember_me = BooleanField('remember_me', default=False)