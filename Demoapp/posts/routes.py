from flask import render_template,url_for,flash,redirect,request,abort,Blueprint
from flask_login import current_user,login_required
from Demoapp import db
from Demoapp.models import Post
from Demoapp.posts.forms import PostForm

posts = Blueprint('posts',__name__)


@posts.route('/post',methods=['GET','POST'])
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
        return redirect(url_for('main.home'))
    return render_template('new_post.html',title='New Post',legend="Create Post",form=form)


@posts.route('/post/<int:post_id>')
def detail_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detail_post.html',title=post.title,post=post)


@posts.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has been Updated",'success')
        return redirect(url_for('posts.detail_post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('update_post.html',title="Update Post",form=form)


@posts.route('/delete/<int:post_id>',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post has been Deleted",'danger')
    return redirect(url_for('main.home'))



@posts.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=5)
    return render_template('user_posts.html',posts=posts,user=user)
