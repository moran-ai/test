"""
app配置
"""
from flask import Flask
from apps.article.views import article_bp1
from apps.user.views import user_bp1
from ext import db, bootstrap
from settings import DevelopmentConfig

# 创建app
def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    # 使用开发环境
    app.config.from_object(DevelopmentConfig)
    # 解决json中文乱码的问题
    app.config['JSON_AS_ASCII'] = False
    # 数据库对象关联app
    db.init_app(app=app)
    # 将bootstrap与app进行关联
    bootstrap.init_app(app)
    # user_p1与app关联
    app.register_blueprint(user_bp1)
    app.register_blueprint(article_bp1)

    return app
