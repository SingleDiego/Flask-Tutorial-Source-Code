from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(Config)
    
    # 初始化各种扩展库
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 引入蓝图并注册
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app

from app import models