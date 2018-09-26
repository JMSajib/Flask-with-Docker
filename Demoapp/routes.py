from flask import render_template,url_for,flash,redirect
from Demoapp import app
from Demoapp.forms import RegistrationForm,LoginForm
from Demoapp.models import Post,User


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'pass12345':
            flash(f'Login Successfull','success')
            return redirect(url_for('home'))
        else:
            flash(f'Invalid Credentials','danger')

    return render_template('login.html',title='Login',form=form)
