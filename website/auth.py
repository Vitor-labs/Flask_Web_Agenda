from flask import Blueprint as bp, render_template as rt, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User
from flask_login import login_user, logout_user, login_required, current_user
from . import db


auth = bp('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form.get('name')
        ps = request.form.get('password')
        print(nome, ps)

        user = User.query.filter_by(username=nome).first()
        if user is None:
            flash('Invalid name', category='error')

        if not check_password_hash(user.password, ps):
            flash('Invalid password', category='error')

        flash('You were successfully logged in', category='success')
        login_user(user, remember=True)

        return redirect(url_for('views.home'))

    return rt('login.html', user=current_user)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password1')
        cpassword = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('User already exists', category='error')
            return redirect(url_for('auth.register'))

        elif len(email) < 10:
            flash('Email must be at least 10 characters long', category='error')
        elif len(name) < 3:
            flash('Name must be at least 3 characters long', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long', category='error')
        elif password != cpassword:
            flash('Passwords do not match', category='error')
        else:
            flash('Successfully registered', category='success')
            new_user = User(email=email, username=name, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            return redirect(url_for('views.home'))

    return rt('singup.html', user=current_user)
