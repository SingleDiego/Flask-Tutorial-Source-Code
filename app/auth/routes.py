from datetime import datetime
from flask import (
    render_template, 
    flash, 
    redirect,
    url_for,
    request,
    current_app
)
from flask_login import (
    login_user, 
    logout_user, 
    current_user,
    login_required
)
from app.auth.forms import (
    LoginForm, 
    RegistrationForm, 
    EditProfileForm
)
from app import db
from app.models import User, Post
from app.auth import auth_routes


@auth_routes.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Sign In', form=form)

@auth_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth_routes.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts_per_page = current_app.config['POSTS_PER_PAGE']
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, 
        posts_per_page, 
        False
    )
    next_url = url_for('auth.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('auth.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(
        'auth/user.html', 
        user=user, 
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )

@auth_routes.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('auth.edit_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template(
        'auth/edit_profile.html', 
        title='Edit Profile',
        form=form
    )

@auth_routes.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('auth.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('auth.user', username=username))

@auth_routes.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('auth.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('auth.user', username=username))