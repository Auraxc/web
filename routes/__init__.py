import uuid
from functools import wraps

import redis
from flask import session, request, abort

from models.user import User
from utils import log


# def current_user():
#     if 'session_id' in request.cookies:
#         session_id = request.cookies['session_id']
#         s = Session.one_for_session_id(session_id=session_id)
#         key = 'session_id_{}'.format(session_id)
#         user_id = int(cache.get(key))
#         log('current_user key <{}> user_id <{}>'.format(key, user_id))
#         u = User.one(id=user_id)
#         return u
#     else:
#         return None

# def current_user():
#     uid = session.get('user_id', '')
#     u: User = User.one(id=uid)
#     # type annotation
#     # User u = User.one(id=uid)
#     return u

def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        # s = Session.one_for_session_id(session_id=session_id)
        key = 'session_id_{}'.format(session_id)
        if cache.get(key) is not None:
            user_id = int(cache.get(key))
            log('current_user key <{}> user_id <{}>'.format(key, user_id))
            u = User.one(id=user_id)
            return u
    else:
        return None


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        csrf_token = 'csrf_token_{}'.format(token)
        k = cache.get(csrf_token)
        if k and int(k) == u.id:
            return f(*args, **kwargs)
        else:
            abort(401)
    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    csrf_token = 'csrf_token_{}'.format(token)
    v = u.id
    cache.set(csrf_token, v)
    return token


cache = redis.StrictRedis()
