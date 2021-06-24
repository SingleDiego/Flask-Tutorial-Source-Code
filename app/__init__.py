from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # 引入蓝图并注册
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app