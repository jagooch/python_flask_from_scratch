from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User,Post
from flaskblog import app

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

@app.route("/register", methods=[ 'GET', 'POST'  ])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect( url_for('home') ) 
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=[ 'GET', 'POST'])
def login():  
    form = LoginForm()
    if form.validate_on_submit():  
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect( url_for('home') ) 
        else:
            flash(f'Login Failed. Check u/p.', 'danger')
    return render_template('login.html', title='Login', form=form)
