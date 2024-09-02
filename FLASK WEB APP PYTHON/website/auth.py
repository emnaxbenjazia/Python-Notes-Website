from flask import Blueprint, render_template, request, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__) 
#nhere we'll define our login, logout, and sign-up routes. We'll also add a prefix to the URL of the auth blueprint. This means that all the routes in the auth blueprint will have '/auth' added to the beginning of their URL. This is useful for organizing our routes and making sure that there are no conflicts between routes in different blueprints.


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #this remembers the fact that this user was logged in until they log out
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user = current_user)


@auth.route('/logout')
@login_required # this means you can only access this route (/logout) if you are logged in
def logout():
    logout_user() 
    return redirect(url_for('auth.login'))



@auth.route('/sign-up', methods=['GET', 'POST']) 
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email invalid', category='error')
        elif len(first_name) < 2:
            flash('First name invalid', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password too short', category='error')
        else:
            #add user to DB
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home')) #the use of url_for is to redirect to a specific route. In this case, we're redirecting to the home route in the views blueprint. we could use '/' instead of 'views.home' but it's better to use the function name in case we change the route in the future.

    return render_template("sign_up.html", user = current_user)