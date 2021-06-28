from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(Config)
    
    # 引入蓝图并注册
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app