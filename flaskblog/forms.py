from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
from flaskblog.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[ DataRequired(), Email(), Length(min=6) ])
    password = PasswordField('Password', validators=[ DataRequired(), Length(min=8)  ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[ DataRequired(), Length(min=2, max=20)  ])
    email = StringField('Email', validators=[ DataRequired(), Email(), Length(min=6)  ])
    password = PasswordField('Password', validators=[ DataRequired(), Length(min=8)  ]) 
    # image_file = ('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username( self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Select a different username.')

    def validate_email( self, email):
        email = User.query.filter_by(username=email.data).first()
        if email:
            raise ValidationError('That email is taken. Select a different email address.')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[ DataRequired(), Length(min=2, max=20)  ])
    email = StringField('Email', validators=[ DataRequired(), Email(), Length(min=6)  ])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])]) 
    submit = SubmitField('Update')

    def validate_username( self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Select a different username.')

    def validate_email( self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Select a different email address.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()] )
    # author = StringField( '', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    # date_posted =  Da


