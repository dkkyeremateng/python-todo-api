from functools import wraps
from flask import request, jsonify

from keep.api.user.models import User


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('X-Auth')

        if token is None:
            return jsonify({}), 401

        user = User.find_by_token(token)

        if not user:
            return jsonify({}), 401

        kwargs['user'] = user

        return f(*args, **kwargs)
    return decorated_function
