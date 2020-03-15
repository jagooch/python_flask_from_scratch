from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User,Post
from flaskblog import app
from flaskblog import db, bcrypt
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required

posts = [
    {
        'author': 'Dova Kin',
        'title': 'First Post',
        'content': 'First post.',
        'date_posted': '20200301'
    },
    {
        'author': 'Angi\'s Cabin',
        'title': 'Second Post',
        'content': 'Second post.',
        'date_posted': '20200302'
    },
    {
        'author': 'Lydia Doorblocker',
        'title': 'Third Post',
        'content': 'I am sworn to carry your burdens.',
        'date_posted': '20200302'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='about')

@app.route("/register", methods=[ 'GET', 'POST' ])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash( form.password.data  ).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account {form.username.data} has been created. You can login. ', 'success')
        return redirect( url_for('login') ) 
    else:
        return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=[ 'GET', 'POST'])
def login():  
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():  
        user = User.query.filter_by(email=form.email.data).first()        
        if user and bcrypt.check_password_hash( user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # if user was trying to go someplace before signing in, direct them to that page.
            return redirect(next_page) if next_page else redirect(url_for('home') )
             
        else:
            flash(f'Login Failed. Check email and password.', 'danger')
    else:
        return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET'])
@login_required
def logout():  
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET'])
@login_required
def account():  
    return render_template('account.html', title='Account')
