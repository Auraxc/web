import uuid

from flask import Blueprint, request, render_template

import config
from models.message import send_mail
from models.user import User
from utils import log

main = Blueprint('reset', __name__)

find = {}


@main.route('/')
def index():
    return render_template("reset/reset.html", message="请输入用户名")


@main.route("/send", methods=['POST'])
def send():
    form = request.form
    username = form['username']
    user = User.one(username=username)
    print('users', user)
    if user is not None:
        user_id = user.id
        print('userid', user_id)
        token = str(uuid.uuid4())
        find[token] = user_id
        subject = '密码找回'
        author = config.admin_mail
        to = user.emailtemp
        content = '请点击链接修改密码 https://www.auramux.com/reset/view?token={}'.format(token)
        send_mail(subject, author, to, content)
    else:
        return render_template("reset/reset.html", message="用户名错误")
    return render_template("reset/reset.html", message="重置邮件已发送，请注意查收")


@main.route('/view', methods=['GET'])
def view():
    token = request.args['token']
    if find[token] is not None:
        uid = find[token]
        u = User.one(id=uid)
        return render_template("reset/update.html", message="请输入新密码", uid=u.id, username=u.username)


@main.route('/update', methods=['POST'])
def update():
    uid = request.form['id']
    password = request.form['password']
    log('pass', password)
    log('user', User.one(id=uid))
    password = User.salted_password(password)
    log('password', password)
    User.update(uid, password=password)
    log(User.one(id=uid))
    return render_template("reset/update.html", message="密码重置成功")
