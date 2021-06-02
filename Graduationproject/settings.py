import os

class Config:
    # flask项目配置文件
    DEBUG = True
    # 创建数据库连接
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:itcast@127.0.0.1:3306/flaskbishe'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # 设置session, 值可以任意取
    SECRET_KEY = 'adfdfggdfhfhfhfhdfhf'
    # 项目路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 静态文件夹的路径
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    # 头像上传目录
    UPLOAD_TOUX_DIR = os.path.join(STATIC_DIR, 'upload\\toux\\')
    # 相册上传目录
    UPLOAD_PHOTO_DIR = os.path.join(STATIC_DIR, 'photo')

# 开发环境
class DevelopmentConfig(Config):
    ENV = 'development'

# 生产环境
class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False

if __name__ == '__main__':
    print(Config.BASE_DIR)
