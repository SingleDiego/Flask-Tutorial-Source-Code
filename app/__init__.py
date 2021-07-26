from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import os
import logging
from logging.handlers import RotatingFileHandler


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config):
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config)
    
    # 初始化各种扩展库
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

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

from app import models