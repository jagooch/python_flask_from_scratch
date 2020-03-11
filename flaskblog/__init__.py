from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from models import User,Post

# Create flask app
app = Flask(__name__)

#set app config
app.config['SECRET_KEY'] = '894f16ed082df645715f80256549fef5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 


#Create database 
db = SQLAlchemy(app)

# create encryption object
bcrypt = Bcrypt(app)

# create login manager 
login_manager = LoginManager(app)

from flaskblog import routes
