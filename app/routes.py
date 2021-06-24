from flask import render_template, Blueprint

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