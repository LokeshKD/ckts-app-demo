###
# Imports
###
from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


###
# App config
###
app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.home.views import home_blueprint

# Register Our BluePrints
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)

from project.models import User
login_manager.login_view = "users.login"

# All non existant pages should bring them to welcome page
@app.errorhandler(404)
def page_not_found(e):
    flash("Page you were looking for does not exist!")
    return redirect(url_for('home.welcome'))

# All unautorized accesses are directed to welcome page
@login_manager.unauthorized_handler
def unauthorized():
    flash("You should login to access that page!!")
    return redirect(url_for('home.welcome'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
