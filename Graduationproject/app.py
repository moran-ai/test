"""
运行文件
"""
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps import create_app
from apps.user.model import User
from apps.article.model import *
from ext import db

app = create_app()

# 配置manager
manager = Manager(app=app)

# 配置migrate, db为自定义的命令，用来完成数据库的映射和迁移
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
