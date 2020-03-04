from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_moment import Moment

bootstrap = Bootstrap()
# 初始化db
db = SQLAlchemy()
moment = Moment()


# 工厂函数，参数为config名字，如development,production,testing
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 根据APP的config参数进行实例化。所以如果意图在shell命令中调控其他DB，那么需要在config里改。
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)

    # 添加路由和自定义的错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


