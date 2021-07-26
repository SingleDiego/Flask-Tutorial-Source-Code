from datetime import datetime
from flask import (
    render_template, 
)
from flask_login import current_user
from app import db
from app.models import User, Post
from app.main import main_routes


@main_routes.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@main_routes.route('/')
@main_routes.route('/index')
def index():

    if current_user.is_active:
        posts = current_user.followed_posts().all()
    else:
        posts = []
        
    return render_template(
        'index.html', 
        title='Home Page', 
        posts=posts
    )