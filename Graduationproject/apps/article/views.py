from flask import render_template, redirect, request, g, Blueprint, url_for, session, jsonify

# 创建蓝图对象
from apps.article.model import Article_type, Article, Comment
from apps.user.model import User
from ext import db

article_bp1 = Blueprint('article', __name__, url_prefix='/article')

# 发表文章
@article_bp1.route('/publish', methods=['GET', 'POST'])
def publish_airutal():
    if request.method == 'POST':
        title = request.form.get('title')
        type_id = request.form.get('type')
        content = request.form.get('content')

        # 放入数据库
        article = Article()
        article.title = title
        article.type_id = type_id
        article.content = content
        article.user_id = g.user.id
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('user.index'))
    types = Article_type.query.all()
    uid = session.get('uid')
    if uid:
        user = User.query.get(uid)
        return render_template('article/airtual.html', types=types, user=user)

# 文章详情页
@article_bp1.route('/detail')
def article_detail():
    """
    文章详情
    :return:
    """
    article_id = request.args.get('aid')
    artlcle = Article.query.get(article_id)
    # 登录用户
    user = None
    user_id = session.get('uid', None)
    if user_id:
        user = User.query.get(user_id)
    # 对评论进行分页
    # 如果page没有找到，默认为1
    page = int(request.args.get('page', 1))
    comments = Comment.query.filter(Comment.article_id == article_id).order_by(-Comment.cdatetime).paginate(page=page, per_page=5)
    return render_template('article/detail.html', article=artlcle, user=user, comments=comments)

# 文章点赞量
@article_bp1.route('/love')
def article_love():
    article_id = request.args.get('aid')
    tag = request.args.get('tag')
    article = Article.query.get(article_id)
    if tag == '1':
        article.love_num -= 1
    else:
        article.love_num += 1
    db.session.commit()
    return jsonify(num = article.love_num)

# 文章收藏量
@article_bp1.route('/save')
def article_save():
    article_id = request.args.get('aid')
    tag = request.args.get('tag')
    article = Article.query.get(article_id)
    if tag == '1':
        article.save_num -= 1
    else:
        article.save_num += 1
    db.session.commit()
    return jsonify(num = article.save_num)

# 文章评论
@article_bp1.route('/comment', methods=['GET', 'POST'])
def article_comment():
    if request.method == 'POST':
        comment_content = request.form.get('comment')
        user_id = g.user.id
        article_id = request.form.get('aid')

        # 评论模型
        comment = Comment()
        # 评论的内容
        comment.comment = comment_content
        # 用户名
        comment.user_id = user_id
        # 文章名
        comment.article_id = article_id
        db.session.add(comment)
        db.session.commit()

        # 得到用户在那一篇文章中发表的评论,回到详情页面
        return redirect(url_for('article.article_detail')+"?aid="+article_id)
    # 返回首页
    return redirect(url_for('user.index'))

# 分章分类查找
@article_bp1.route('/type_search')
def type_search():
    # 用户对象的判断
    uid = session.get('uid')
    user = None
    if uid:
        user = User.query.get(uid)

        # 文章分类获取
        types = Article_type.query.all()

        # tid获取
        tid = request.args.get('tid', 1)

        # 获取文章类型
        type = Article_type.query.get(tid)
    return render_template('article/airtual_type.html', user=user, types=types, type=type)

# 关键字搜索
@article_bp1.route('/search')
def search():
    keyword = request.args.get('search')
    print('关键字是：--------->', keyword)
    print('关键字的类型是：--------->', type(keyword))
    uid = session.get('uid')
    if uid:
        user = User.query.get(uid)
        article = Article.query.filter(Article.title.contains(keyword))
        page = int(request.args.get('page', 1))

        # paginate(page, per_page) 函数对文章进行分页 参数:page:当前页面是第多少页， per_page每页的个数
        # articles = Article.query.order_by(-Article.pdatetime).all()  # 按照文章的发布日期进行排序
        pagination = Article.query.filter(Article.title.contains(keyword)).order_by(-Article.pdatetime).paginate(page=page, per_page=4)
        return render_template('article/search.html', articles=article, user=user, pagination=pagination)
