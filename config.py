import os


# 基础配置
class Config:
    # 表单加密需要 跨站请求伪造保护
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'really hard to guess!'

    # 数据库配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 动态追踪修改设置，如未设置会Warning
    SQLALCHEMY_ECHO = False  # 查询时是否显示原始SQL语句

    @staticmethod
    def init_app(app):
        pass


# 继承Config
class DevelopmentConfig(Config):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/safeGuard?charset=UTF8MB4'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Jjh116023@http://rm-bp1m0v39119u248032o.mysql.rds.aliyuncs.com:3306/safeGuard?charset=UTF8MB4'


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
