import os
import time
import uuid

import gevent
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory,
    current_app
)
from flask_sqlalchemy import SQLAlchemy

from werkzeug.datastructures import FileStorage

from models.base_model import db
from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import current_user, cache
# from routes import current_user

import json

from utils import log

main = Blueprint('index', __name__)

"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():

    time.sleep(0.1)
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    # 用类函数来判断
    User.register(form)

    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        session_id = str(uuid.uuid4())
        key = 'session_id_{}'.format(session_id)
        log('index login key <{}> user_id <{}>'.format(key, u.id))
        cache.set(key, u.id)
        redirect_to_index = redirect(url_for('topic.index'))
        response = current_app.make_response(redirect_to_index)
        response.set_cookie('session_id', value=session_id)
        # 转到 topic.index 页面
        return response
        # session['user_id'] = u.id
        # return redirect(url_for('topic.index'))


def created_topic(user_id):
    topic = Topic.all(user_id=user_id)
    topic = sorted(topic, key=lambda m: m.created_time, reverse=True)
    return topic


def replied_topic(user_id):

    replied = Reply.all(user_id=user_id)
    replied = sorted(replied, key=lambda m: m.created_time, reverse=True)
    print('replied', replied)
    return replied


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        # 获取发布的 topic
        topic = created_topic(u.id)
        # 获取参与的 topic
        replied = replied_topic(u.id)

        return render_template(
            'profile.html',
            user=u,
            topic=topic,
            replied=replied,
        )


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        return render_template('profile.html', user=u)


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']
    # file = request.files['avatar']
    # filename = file.filename
    # ../../root/.ssh/authorized_keys
    # images/../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    if suffix not in ['gif', 'jpg', 'jpeg']:
        abort(400)
        log('不接受的后缀, {}'.format(suffix))
    else:
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        path = os.path.join('images', filename)
        file.save(path)

        u = current_user()
        User.update(u.id, image='{}'.format(filename))

        return redirect(url_for('.profile'))


@main.route('/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # http://localhost:3000/images/..%5Capp.py
    # path = os.path.join('images', filename)
    # print('images path', path)
    # return open(path, 'rb').read()
    # if filename in os.listdir('images'):
    #     return

    return send_from_directory('images', filename)


@main.route('/setting')
def setting():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template(
            'setting.html',
            user=u
        )


@main.route('/update_setting', methods=['POST'])
def update_setting():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        form = request.form
        bio = form['bio']
        username = form['username']
        User.update(u.id, bio=bio, username=username)
        print('bio', User.bio)
        print('username', User.username)
        return redirect(url_for('.setting'))


@main.route('/update_password', methods=['POST'])
def update_password():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        form = request.form
        print('form', form, u.password, form['old_pass'])
        old_pass = User.salted_password(form['old_pass'])
        if u.password == old_pass:
            print('right')
            new_pass = User.salted_password(form['new_pass'])
            User.update(u.id, password=new_pass)
            return redirect(url_for('.setting'))
        return redirect(url_for('.setting'))


@main.route('/about')
def about():
    return render_template('about.html')
