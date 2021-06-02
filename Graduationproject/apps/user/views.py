import os

from flask import Blueprint, render_template, request, url_for, redirect, jsonify, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from apps.article.model import Article_type, Article
from apps.user.model import User
from ext import db
from settings import Config

# from flask import Blueprint
# 创建蓝图对象
user_bp1 = Blueprint('user', __name__, url_prefix='/user')

# 设定请求登录的列表
required_login_list = ['/user/center',
                       '/user/change',
                       '/article/publish',
                       '/article/comment',
                       '/user/upload',
                       '/user/l_img',
                       '/article/type_search',
                       '/article/search',
                       '/article/love',
                       '/article/save']


# 设定钩子函数
@user_bp1.before_app_request
def app_request():
    """
    该请求会执行多次
    :return:
    """
    # print('before_app_request', request.path)
    if request.path in required_login_list:
        id = session.get('uid')
        if not id:
            return render_template('user/login.html')
        else:
            user = User.query.get(id)
            g.user = user


# 自定义过滤器
@user_bp1.app_template_filter('cdecode')
def content_decode(content):
    # content = content.encode('utf-8')
    # 确定首页文章展示字数
    return content[:200]


# 首页
@user_bp1.route('/')
def index():
    # 1. 获取登录后首页的cookie值,默认值为None
    # uid = request.cookies.get('uid', None)
    # 2. session的获取  session底层会自动获取
    uid = session.get('uid')

    # 获取文章列表
    # 获取页码数, 默认值为1
    page = int(request.args.get('page', 1))

    # paginate(page, per_page) 函数对文章进行分页 参数:page:当前页面是第多少页， per_page每页的个数
    # articles = Article.query.order_by(-Article.pdatetime).all()  # 按照文章的发布日期进行排序
    pagination = Article.query.order_by(-Article.pdatetime).paginate(page=page, per_page=4)  # 按照文章的发布日期进行排序
    print(pagination.items)  # 每页的文章条数 返回list [<Article 4>, <Article 3>, <Article 2>, <Article 1>]
    print(pagination.page)  # 当前页码数
    print(pagination.prev_num)  # 前一页的页码数
    print(pagination.next_num)  # 后一页的页码数
    print(pagination.has_next)  # 是否有下页 返回值为boolean
    print(pagination.has_prev)  # 是否有上页 返回值为boolean
    print(pagination.pages)  # 总页数
    print(pagination.total)  # 数据库中的总页数
    # 获取分类列表
    # types = Article.query.all()
    # 判断用户是否登录
    if uid:
        # 通过主键查找用户，将用户展示到主页
        user = User.query.get(uid)
        # return render_template('user/index.html', user=user, articles=articles, type=types)
        return render_template('user/index.html', user=user, pagination=pagination)
    else:
        # return render_template('user/index.html', articles=articles, type=types)
        return render_template('user/index.html', pagination=pagination)


# 用户注册
@user_bp1.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册
    :return:
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        email = request.form.get('email')
        if password == repassword:
            # 创建数据库对象
            user = User()
            user.username = username
            # user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            # 使用自带的generate_password_hash函数加密，底层使用sha256加密
            user.password = generate_password_hash(password)
            user.phone = phone
            user.email = email
            # 将数据添加数据库
            db.session.add(user)
            # 提交
            db.session.commit()
            return render_template('user/go_back.html', msg='注册成功,点击返回首页')
    return render_template('user/register.html')


# 用户登录
@user_bp1.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # 用户名或者密码登录
        username = request.form.get('username')
        password = request.form.get('password')
        users = User.query.filter(User.username == username).all()
        for user in users:
            # 检查密码是否一致 返回值为boolean
            flag = check_password_hash(user.password, password)
            if flag:
                # 1.cookie机制
                # response = redirect(url_for('user.index'))
                # # 设置cookie，记录登录状态
                # # max_age表示记录最大存活时间，以秒为单位
                # response.set_cookie('uid', str(user.id), max_age=1800)
                # return response

                # 2.session机制
                session['uid'] = user.id
                return redirect(url_for('user.index'))
        else:
            return render_template('user/login.html', msg='用户名或密码错误')
    return render_template('user/login.html')


# 手机号码验证
@user_bp1.route('/checkphone', methods=['POST', 'GET'])
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()
    if len(user) > 0:
        return jsonify(code=400, msg='此号码已被注册')
    else:
        return jsonify(code=200, msg='此号码可用')


# 密码长度校验
@user_bp1.route('/checkpasswordlength', methods=['GET', 'POST'])
def check_password():
    password = request.args.get('password')
    user = User.query.filter(User.password == password).all()
    if len(user) < 6:
        return jsonify(code=400, msg='密码长度不合法')
    else:
        return jsonify(code=200, msg='ok')


# 用户退出
@user_bp1.route('/logout')
def logout():
    # 1.cookie的方式
    # response = redirect(url_for('user.index'))
    # delete_cookie(key)  key是要删除的cookie的key
    # response.delete_cookie('uid')
    # return response

    # 2.session的方式
    # del session
    session.clear()
    return redirect(url_for('user.index'))


# 用户中心
@user_bp1.route('/center')
def user_center():
    return render_template('user/center.html', user=g.user)


# 允许上传的文件扩展名
ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif', 'bmp', 'jpeg', 'JPG', 'PNG', 'GIF', 'JPEG', 'BMP']


# 用户信息修改
@user_bp1.route('/change', methods=['GET', 'POST'])
def user_change():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        # 图片的获取方式,request.files.get('名字')
        touxiang = request.files.get('file')
        print('------->', touxiang)  # <FileStorage
        # 属性 filename:用户获取文件的名字
        # 方法：save(save_path)
        t_name = touxiang.filename  # 获取文件名字
        # 判断图片的扩展名
        if t_name.rsplit('.')[-1] in ALLOWED_EXTENSIONS:  # 对获取的图片名字进行切割，取出图片的格式
            t_name = secure_filename(t_name)  # 保证文件名符合python命名规则
            # 拼接上传图片路径
            file_path = os.path.join(Config.UPLOAD_TOUX_DIR, t_name)
            touxiang.save(file_path)
            # 保存成功
            # 保存到数据库
            user = g.user  # g.user是一个对象，给对象赋予属性值
            user.username = username
            user.phone = phone
            user.email = email
            path = 'upload/toux/'
            user.icon = os.path.join(path, t_name)
            db.session.commit()
            return redirect(url_for('user.user_center'))
        else:
            return render_template('user/center.html', user=g.user, msg='文件格式仅限于jpg, png, bmp, gif')
    return render_template('user/center.html', user=g.user)


# 相册
@user_bp1.route('/upload', methods=['GET', 'POST'])
def upload():
    uid = session.get('uid')
    if uid:
        user = User.query.get(uid)
    if request.method == 'POST':
        file = request.files.get('file')
        print('file的类型为:------->', type(file))
        f = file.filename
        print('上传的文件名为：------------>', f)
        f_name = f.rsplit('.')[-1]
        if f_name in ALLOWED_EXTENSIONS:
            secure_filename(f_name)
            f_path = os.path.join(Config.UPLOAD_PHOTO_DIR, f)
            file.save(f_path)
            return render_template('user/photo.html', imgs=os.listdir('./static/photo'))
        else:
            return jsonify({'msg': '仅支持jpg, png, gif, bmp, jpeg, JPG, PNG, GIF, JPEG, BMP格式的文件上传，请重新选择文件'})
    return render_template('user/photo.html', user=user)


# 查看相册里的图片
@user_bp1.route('/l_img')
def l_img():
    uid = session.get('uid')
    if uid:
        user = User.query.get(uid)
    imgss = os.listdir('./static/photo')
    return render_template('user/img_loo.html', imgs=imgss, user=user)
