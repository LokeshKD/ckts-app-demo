
from flask import flash, redirect, url_for, request, render_template, \
    Blueprint
#from functools import wraps
from flask_login import login_user, login_required, logout_user
from project.users.form import LoginForm, RegisterForm
from project import db
from project.models import User, bcrypt

###
# Config
###

users_blueprint = Blueprint('users', __name__,
                        template_folder = 'templates')

###
# Helper Functions
###
'''
#login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['username']).first()

            if user is not None and bcrypt.check_password_hash(
                        user.password, request.form['password']):
                #session['logged_in'] = True
                login_user(user)
                flash('You were just logged in')
                return redirect(url_for('home.home'))
            else:
                error = 'Invalid Credentials. Please Try again'
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/logout')
@login_required
def logout():
    #session.pop('logged_in', None)
    logout_user()
    flash('You were just logged out')
    return redirect(url_for('home.welcome'))

@users_blueprint.route('/register', methods=['GET', 'POST']) # pragma: no cover
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data,
            birth_date=form.birth_date.data,
            mobile=form.mobile.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home.home'))
    return render_template('register.html', form=form)
