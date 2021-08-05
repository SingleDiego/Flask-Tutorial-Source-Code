from flask import (
    render_template, 
    flash,
    redirect,
    url_for,
    request,
    current_app
)
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.main import main_routes
from app.main.forms import PostForm
from flask_babel import _


@main_routes.route('/', methods=['GET', 'POST'])
@main_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts_pre_page = current_app.config['POSTS_PER_PAGE']
    posts = current_user.followed_posts() \
        .paginate(page, posts_pre_page, False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(
        'index.html', 
        title='Home Page', 
        form=form,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )

@main_routes.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts_pre_page = current_app.config['POSTS_PER_PAGE']
    posts = Post.query \
        .order_by(Post.timestamp.desc()) \
        .paginate(page, posts_pre_page, False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(
        'index.html', 
        title='Explore', 
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )

