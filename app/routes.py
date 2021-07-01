from flask import (
    render_template, 
    Blueprint, 
    flash, 
    redirect,
    url_for
)
from app.forms import LoginForm


main_routes = Blueprint('main', __name__)

@main_routes.route('/')
@main_routes.route('/index')
def index():
    user = {'username': 'Diego'}

    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Hello World!'
        },
        {
            'author': {'username': 'Diego'},
            'body': 'Hola Wolrd!'
        }
    ]

    return render_template(
        'index.html', 
        title='Home', 
        user=user, 
        posts=posts
    )


@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)