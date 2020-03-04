from flask import Flask
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
import sqlite3
from pprint import pprint
from forms import RegistrationForm, LoginForm


with sqlite3.connect("posts.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select * from posts")
    posts = [ dict(row) for row in cursor.fetchall()]

pprint(posts)

app = Flask(__name__)
app.config['SECRET_KEY'] = '894f16ed082df645715f80256549fef5'


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

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)



if __name__ == "__main__":
    app.run(debug=True)