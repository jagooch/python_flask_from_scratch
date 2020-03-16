from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User,Post
from flaskblog import app
from flaskblog import db, bcrypt
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required
import secrets
import os 
from PIL import Image

posts = [
    {
        'author': 'Dova Kin',
        'title': 'For the Nords',
        'content': 'Skyrim is for the Nords.',
        'date_posted': '20200301'
    },
    {
        'author': 'Angi\'s Cabin',
        'title': 'Practice',
        'content': 'You need more practice. Here are some practice arrows.',
        'date_posted': '20200302'
    },
    {
        'author': 'Lydia Doorblocker',
        'title': 'Housecarl Duties?',
        'content': 'I will protect you, and all you own, with my life.',
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

def save_picture( form_picture ):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f'{random_hex}{f_ext}'
    picture_path = os.path.join( app.root_path, 'static/profile_pics', picture_fn )
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    # form_picture.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():  
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data) 
            current_user.image_file = picture_file
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect( url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}' )
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():  
    form = PostForm()
    if form.validate_on_submit():
        flash('Your post has been created!', 'success')
        return redirect( url_for('home') )
    else:
        return render_template('create_post.html', title='New Post', form=form)
