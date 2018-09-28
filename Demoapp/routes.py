import secrets
import os
from PIL import Image
from flask import render_template,url_for,flash,redirect,request
from Demoapp import app,db,bcrypt
from Demoapp.forms import RegistrationForm,LoginForm,UpdateAccountForm,PostForm
from Demoapp.models import Post,User
from flask_login import login_user,current_user,logout_user,login_required


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html',posts=posts)


@app.route('/about')
def about():
    return render_template('about.html',title='About')


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=username,email=email,password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account has been Created','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
                return redirect(url_for('home'))
        else:
            flash(f'Invalid Credentials','danger')

    return render_template('login.html',title='Login',form=form)


@app.route('/logout')
def logout():
    flash(f'Logout Successfully','success')
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    randorm_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = randorm_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/account',methods=['GET','POST'])
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
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Acount',image_file=image_file,form=form)


@app.route('/post',methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(title=title,content=content,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post has been Created Successfully','success')
        return redirect(url_for('home'))
    return render_template('new_post.html',title='New Post',form=form)
