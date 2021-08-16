from datetime import datetime
from langdetect import detect

from flask import (
    render_template, 
    flash,
    redirect,
    url_for,
    request,
    current_app,
    g,
    jsonify
)
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.main.forms import PostForm, SearchForm
from app.translate import translate
from app.main import main_routes

@main_routes.before_app_request
def before_app_request():
    if str(get_locale()) == 'zh':
        local = 'zh-CN'
    else:
        local = 'en'
    g.locale = local

    if current_user.is_authenticated:
        g.search_form = SearchForm()

@main_routes.route('/', methods=['GET', 'POST'])
@main_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        try:
            language = detect(form.post.data)
        except:
            language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
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

@main_routes.route('/translate', methods=['POST'])
@login_required
def translate_text():
    text = request.form['text']
    source_language = request.form['source_language']
    dest_language = request.form['dest_language']
    result = translate(text, source_language, dest_language)
    return jsonify(result)

@main_routes.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))

    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(
        g.search_form.q.data, 
        page,
        current_app.config['POSTS_PER_PAGE']
    )
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None

    return render_template(
        'search.html', 
        title=_('Search'), 
        posts=posts,
        next_url=next_url, 
        prev_url=prev_url
    )