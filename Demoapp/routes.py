from flask import render_template,url_for,flash,redirect,request
from Demoapp import app,db,bcrypt
from Demoapp.forms import RegistrationForm,LoginForm,UpdateAccountForm
from Demoapp.models import Post,User
from flask_login import login_user,current_user,logout_user,login_required


posts = [
    {
        'author':'Sajib',
        'title':'New Title',
        'content':'This is a Brand New Content'
    },
    {
        'author':'Jahidul',
        'title':'New Title2',
        'content':'This is a Brand New Content2'
    }
]


@app.route('/')
def home():
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


@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
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
