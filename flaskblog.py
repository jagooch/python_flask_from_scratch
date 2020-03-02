from flask import Flask
from flask import render_template
app = Flask(__name__)

posts = [
    {
        'author': 'John Gooch'
        'title': 'First Post'
        'date_posted': 
    }







]





@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')



if __name__ == "__main__":
    app.run(debug=True)