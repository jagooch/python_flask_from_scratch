from flask import Flask
from flask import render_template
import sqlite3
from pprint import pprint


with sqlite3.connect("posts.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select * from posts")
    posts = [ dict(row) for row in cursor.fetchall()]

pprint(posts)

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='about')

if __name__ == "__main__":
    app.run(debug=True)