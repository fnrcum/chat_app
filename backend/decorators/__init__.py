from functools import wraps
from jose import JWTError, jwt
from flask import request, g, current_app, abort
from datetime import datetime
from models._models import User


def login_required(f):
    """
    This decorator checks the header to ensure a valid token is set
    """
    @wraps(f)
    def func(*args, **kwargs):
        try:
            if 'authorization' not in request.headers:
                abort(400, message="You need to be logged in to access this resource")
            token = request.headers.get('authorization') or request.cookies.get("token")
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            expiration = payload['date_time']
            if datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S") < datetime.now():
                abort(400, message="Token expired, please relog in")
            user_id = payload['id']
            g.user = User.find(user_id)
            if g.user is None:
               abort(404, message="The user id is invalid")
            return f(*args, **kwargs)
        except JWTError as e:
            abort(400, message="There was a problem while trying to parse your token -> {}".format(e.message))
    return func


def validate_user(f):
    """
    This decorate ensures that the user logged in is the actually the same user we're operating on
    """
    @wraps(f)
    def func(*args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id != g.user['id']:
            abort(404, message="You do not have permission to the resource you are trying to access")
        return f(*args, **kwargs)
    return func