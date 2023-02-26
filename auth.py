from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Please Enter correct Credentials!')
            return redirect(url_for('auth.login'))

        elif not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.scan'))


@auth.route('/addUser', methods=['GET', 'POST'])
# @login_required
def addUser():
    if request.method == 'GET':
        return render_template('addUser.html')
    else:
        role = request.form.get('role')
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        re_password = request.form.get('re-password')
        if password == re_password:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email address already exists')
                return redirect(url_for('auth.addUser'))
            flash('Added Successfully!')
            new_user = User(email=email, name=name, password=generate_password_hash(
                password, method='sha256'), role=role)
            # adding in database of user
            db.session.add(new_user)
            db.session.commit()
        else:
            flash("PassWord Doesn't match!")
            return redirect(url_for('auth.addUser'))
        return redirect(url_for('auth.addUser'))


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def Profile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        db.session.query(User).filter_by(id=current_user.id).update(
            {"name": name, "email": email})
        db.session.commit()
    return render_template('profile.html')


@auth.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        if request.form.get('accountActivation') == 'delete':
            user = User.query.filter_by(id=current_user.id).one()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash('Please confirm!')
    return render_template('profile.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
