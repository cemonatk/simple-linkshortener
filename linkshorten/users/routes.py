from linkshorten import db, bcrypt
from linkshorten.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request, Blueprint
from linkshorten.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
users = Blueprint('users', __name__)

@users.route("/page/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/page/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/page/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/page/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            return render_template('account.html', title='Account Information Updated!', form=form)
        else:
            logout_user()
            return render_template('home.html', title='Password was incorrect!')

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)