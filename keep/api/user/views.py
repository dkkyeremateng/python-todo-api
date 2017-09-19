from flask import Blueprint

from keep.api.user.api import UserAPI

user = Blueprint('user', __name__, url_prefix='/api')

user_view = UserAPI.as_view('user_api')

user.add_url_rule('/users/me',
                  view_func=user_view, methods=['GET', ])

user.add_url_rule('/users/login',
                  view_func=user_view, methods=['POST', ])

user.add_url_rule('/users/',
                  view_func=user_view, methods=['POST', ])

user.add_url_rule('/users/me/token',
                  view_func=user_view, methods=['DELETE'])
