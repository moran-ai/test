"""
数据库模型文件
"""
from datetime import datetime

# 导入数据库对象
from ext import db

# 创建用户表
class User(db.Model):
    # primary_key=True 主键  autoincrement=True 自增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # nullable=False 不允许为空
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # unique=True 唯一
    phone = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(30))
    # 用户头像
    icon = db.Column(db.String(100))
    # default 默认值
    rdatetime = db.Column(db.DateTime, default=datetime.now)

    # 增加一个字段,relationship体现在view和templates上
    articles = db.relationship('Article', backref='user')

    # 文章评论
    comments = db.relationship('Comment', backref='user')

    def __str__(self):
        return self.username
