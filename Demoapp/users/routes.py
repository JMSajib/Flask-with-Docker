from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Demoapp import db, bcrypt
from Demoapp.models import User, Post
from Demoapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from Demoapp.users.utils import save_picture, send_reset_email


users = Blueprint('users',__name__)


@users.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=username,email=email,password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account has been Created','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='Register',form=form)


@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash(f'Login Successfull','success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash(f'Invalid Credentials','danger')

    return render_template('login.html',title='Login',form=form)


@users.route('/logout')
def logout():
    flash(f'Logout Successfully','success')
    logout_user()
    return redirect(url_for('main.home'))



@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Account has been Updated",'success')
        return redirect(url_for('main.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Acount',image_file=image_file,form=form)



@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An Email has been Sent with Specific Instruction",'success')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title='Reset Password',form=form)


@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash("Thast is an Invalid or Expired Token",'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your Password has been Updated!!")
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title='Reset Password',form=form)