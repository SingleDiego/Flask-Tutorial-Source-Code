from flask import Flask, request, current_app
from config import Config
from app.cli import translate

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, _, lazy_gettext as _l

import os
import logging
from logging.handlers import RotatingFileHandler
from elasticsearch import Elasticsearch


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()

login = LoginManager()
login.login_view = "auth.login"
login.login_message = _l("Please log in to access this page.")

def create_app(config):
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config)
    
    # 初始化各种扩展库
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    
    # 绑定命令
    app.cli.add_command(translate)

    # 设置全局搜索 elasticsearch
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    # 日志设定
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        app.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(
            'logs/microblog.log',
            maxBytes=10240, 
            backupCount=10
        )
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.info("Microblog startup!")

    # 引入蓝图并注册
    from app.main.routes import main_routes
    app.register_blueprint(main_routes)

    from app.auth.routes import auth_routes
    app.register_blueprint(auth_routes)

    from app.errors.routes import errors_routes
    app.register_blueprint(errors_routes)

    return app

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    # return 'en'

from app import models